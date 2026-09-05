import logging, config_loader

def get_logger() -> logging.Logger:
    logger = logging.getLogger('HospitalSystem')
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        logger.handlers.clear()

    config = config_loader.load_config('config.json')
    log_file = config.get("log_file", "hospital_system.log")
    
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(name)s - %(message)s')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
