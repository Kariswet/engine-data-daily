from config.db import DatabaseManager
from datetime import datetime
from pymongo import UpdateOne
from loguru import logger

import yfinance as yf
import pandas as pd
import uuid
import json
import time
import os

class StockService:
    def __init__(self):
        self.config = DatabaseManager()

    def _get_stock_code(self):
        code_df = pd.read_excel("data/stock_data.xlsx")
        code_str = code_df["Stock Code"].to_json("data/stock_code.json", orient="records", indent=4)
        
        return code_str


    def OHLCVdaily(self):
        self.db = os.getenv("MONGODB_NAME")
        self.coll_name = "ohlcv_daily"
        self.mongo = self.config.get_mongo_collection(self.db, self.coll_name)
        
        with open("data/stock_code.json", "r") as json_file:
            data = json.load(json_file)
        
        idx_code = [item + ".JK" for item in data]
        logger.info(len(idx_code))

        for i in range(0, len(idx_code), 50):
            batch = idx_code[i : i + 50]            

            downloader = yf.download(batch, period="1d", group_by="ticker", threads=True)
            ops = []
            
            for code in batch:
                if code in downloader and not downloader[code].empty:
                    df_single = downloader[code].dropna()
                    code_clear = code.replace(".JK", "")
                    # print("df_single: ", df_single)

                    for index, row in df_single.iterrows():
                        # print("index: ", index)
                        # print("row: ", row)
                        new_id = int(index.timestamp() * 1000)
                        doc = {
                            "_id": f"{code_clear}_{new_id}",
                            "ticker": code_clear,
                            "date": int(index.timestamp() * 1000),
                            "open": float(row["Open"]),
                            "high": float(row["High"]),
                            "low": float(row["Low"]),
                            "close": float(row["Close"]),
                            "volume": int(row["Volume"]),
                            "updated_at": int(datetime.now().timestamp() * 1000),
                        }
                        
                        ops.append(
                            UpdateOne(
                                {"_id": doc["_id"]},
                                {"$set": doc},
                                upsert=True
                            )
                        )
            if ops:
                self.mongo.bulk_write(ops)
                logger.info(f"Batch {i//50 + 1}: Success storing {len(ops)} stock data.")

            time.sleep(1)
            
    def FINANCEreport(self):
        self.db = os.getenv("MONGODB_NAME")
        self.coll_name = "fundamental"
        self.mongo = self.config.get_mongo_collection(self.db, self.coll_name)

        with open("data/stock_code.json", "r") as json_file:
            data = json.load(json_file)
        
        idx_code = [item + ".JK" for item in data]
        logger.info("Start updating fundamental data..")

        ops = []

        
        for index, code in enumerate(idx_code):
            try:
                info = yf.Ticker(code).info
                
                if not info or "marketCap" not in info:
                    continue
                
                code_clear = code.replace(".JK", "")
                custom_id = f"{code_clear}_fundamental"

                doc = {
                    "_id": custom_id,
                    "market_cap": info.get("marketCap", 0),
                    "trailing_pe": info.get("trailingPE", 0),
                    "forward_pe": info.get("forwardPE", 0),
                    "price_to_book": info.get("priceToBook", 0),
                    "return_on_equity": info.get("returnOnEquity", 0),
                    "profit_margins": info.get("profitMargins", 0),
                    "debt_to_equity": info.get("debtToEquity", 0),
                    "revenue_growth": info.get("revenueGrowth", 0),
                    "earnings_growth": info.get("earningsGrowth", 0),
                    "dividend_yield": info.get("dividendYield", 0),
                    "beta": info.get("beta", 0),
                }

                logger.info(doc)

                ops.append(
                    UpdateOne(
                        {"_id": doc["_id"]},
                        {"$set": doc},
                        upsert=True
                    )
                )    
            except Exception as e:
                logger.info(f"Failed get fundamental {code}: {e}")

            time.sleep(1)

            if len(ops) >= 50:
                self.mongo.bulk_write(ops)
                ops = []
                logger.info(f"Progress fundamental: processing {index + 1}/{len(idx_code)} data...")
        
        if ops:
            self.mongo.bulk_write(ops)
        
        logger.info("Done! Update data Fundamental")