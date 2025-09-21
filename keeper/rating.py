# app/routers/rating.py

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from database import get_db_connection
from models import BlueRatingCreate, BlueRating, BlueRatingHistoryResponse, ShopItem, PurchaseRequest, RedCoinsUpdate

router = APIRouter(prefix="/rating", tags=["Rating & Shop"])

@router.get("/employees/{employee_id}/blue-rating-history/", response_model=BlueRatingHistoryResponse)
def get_blue_rating_history(employee_id: int, period: Optional[str] = None):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, bcoins FROM employees WHERE id = %s", (employee_id,))
            employee = cur.fetchone()
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")
            
            query = "SELECT * FROM blue_rating WHERE employee_id = %s"
            params = [employee_id]
            
            if period and period.endswith('d'):
                days = int(period[:-1])
                query += " AND created_at >= CURRENT_TIMESTAMP - INTERVAL '%s days'"
                params.append(days)
            
            query += " ORDER BY created_at DESC"
            
            cur.execute(query, params)
            history = cur.fetchall()
            
            return {
                "total_bcoins": employee['bcoins'],
                "history": history
            }

@router.patch("/employees/{employee_id}/blue-rating/", response_model=BlueRating)
def update_blue_rating(employee_id: int, rating_data: BlueRatingCreate):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            cur.execute("UPDATE employees SET bcoins = bcoins + %s WHERE id = %s", (rating_data.delta, employee_id))
            
            cur.execute("""
                INSERT INTO blue_rating (employee_id, delta, reason, created_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                RETURNING *
            """, (employee_id, rating_data.delta, rating_data.reason))
            
            new_rating = cur.fetchone()
            conn.commit()
            
            return new_rating

@router.get("/shop/", response_model=List[ShopItem])
def get_shop_items():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM shop_items WHERE is_available = TRUE ORDER BY price_rcoins")
            items = cur.fetchall()
            return items

@router.post("/shop/{item_id}/purchase/")
def purchase_shop_item(item_id: int, purchase_data: PurchaseRequest):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, rcoins FROM employees WHERE id = %s", (purchase_data.employee_id,))
            employee = cur.fetchone()
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")
            
            cur.execute("SELECT * FROM shop_items WHERE id = %s AND is_available = TRUE", (item_id,))
            item = cur.fetchone()
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            
            total_price = item['price_rcoins'] * purchase_data.quantity
            if employee['rcoins'] < total_price:
                raise HTTPException(status_code=400, detail="Not enough rcoins")
            
            cur.execute("UPDATE employees SET rcoins = rcoins - %s WHERE id = %s", (total_price, purchase_data.employee_id))
            
            cur.execute("""
                INSERT INTO purchases (employee_id, shop_item_id, quantity)
                VALUES (%s, %s, %s)
                RETURNING *
            """, (purchase_data.employee_id, item_id, purchase_data.quantity))
            
            purchase = cur.fetchone()
            conn.commit()
            
            return {
                "message": "Purchase successful",
                "purchase_id": purchase['id'],
                "item_name": item['name'],
                "quantity": purchase_data.quantity,
                "total_cost": total_price,
                "remaining_rcoins": employee['rcoins'] - total_price
            }

@router.patch("/employees/{employee_id}/red-coins/")
def update_red_coins(employee_id: int, update_data: RedCoinsUpdate):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, rcoins FROM employees WHERE id = %s", (employee_id,))
            employee = cur.fetchone()
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")
            
            new_balance = employee['rcoins'] + update_data.delta
            cur.execute("UPDATE employees SET rcoins = %s WHERE id = %s", (new_balance, employee_id))
            
            conn.commit()
            
            return {
                "message": "Red coins updated",
                "employee_id": employee_id,
                "delta": update_data.delta,
                "new_balance": new_balance,
                "reason": update_data.reason
            }