import time
import gc
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from src.config.logs_config import setup_log, auto_logger

logger = setup_log(name="Hardware_Manager", filename="utils")

@auto_logger(logger)
def hardware_optimized_models(imbalance_ratio, use_gpu=False):

    logger.info(f"Configuring models. Target hardware environment: {'GPU (CUDA)' if use_gpu else 'CPU (Multi-threading)'}")

    models = {
            "Logistic Regression (SGD)": SGDClassifier(
                loss='log_loss', 
                penalty='l2', 
                max_iter=1000, 
                random_state=42),
            "Random Forest": RandomForestClassifier(
                n_estimators=200, 
                class_weight='balanced', 
                n_jobs=-1, 
                random_state=42)
            }

    if use_gpu:
        models.update({
            "XGBoost": XGBClassifier(
                tree_method='hist', 
                device='cuda', 
                n_estimators=200, 
                max_depth=10, 
                learning_rate=0.1, 
                subsample=0.8,
                colsample_bytree=0.8,
                scale_pos_weight=10,
                random_state=42),
            "LightGBM": LGBMClassifier(
                device_type='gpu', 
                n_estimators=200, 
                learning_rate=0.1,
                max_depth=10, num_leaves=31,
                subsample=0.8,
                colsample_bytree=0.8,
                class_weight='balanced',
                random_state=42),
            "CatBoost": CatBoostClassifier(
                task_type='GPU',
                iterations=200,
                depth=10,
                auto_class_weights='Balanced',
                verbose=0,
                random_seed=42)
            })
    else:
        # Cấu hình chuẩn xác 100% theo Jupyter Notebook của Team 3 cho môi trường CPU
        models.update({
            "XGBoost": XGBClassifier(
                tree_method='hist',
                n_estimators=200,
                max_depth=10,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                scale_pos_weight=10,
                random_state=42,
                eval_metric='logloss',
                n_jobs=-1),
            "LightGBM": LGBMClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=10,
                num_leaves=31,
                subsample=0.8,
                colsample_bytree=0.8,
                class_weight='balanced',
                objective='binary',
                random_state=42,
                n_jobs=-1),
            "CatBoost": CatBoostClassifier(
                iterations=200,
                depth=6,
                auto_class_weights='Balanced',
                eval_metric='AUC',
                thread_count=-1,
                verbose=0,
                random_seed=42) # Ép depth=6 để chống treo máy
            })

    return models

@auto_logger(logger)
def free_resoucre_and_cooldown(sec=0):
    logger.info("Initiating hardware resource cleanup")

    # Ép python phải dọn ram ngay để chuẩn bị cho model tiếp theo
    collected = gc.collect()
    logger.info(f"Garbage collector freed {collected} objects from memory")

    if sec > 0:
        logger.info(f"Thermal cooldown activated. Pausing execution for {sec} seconds")
        time.sleep(sec)
        logger.info("Cooldown complete. Hardware temperatures stabilized. Resuming operation")
    else:
        logger.info("Cooldown skipped. Proceeding immediately")
