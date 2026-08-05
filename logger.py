import logging

def get_logger():
    logger = logging.getLogger('HospitalSystem')
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        logger.handlers.clear()
    
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(name)s - %(message)s')
    file_handler = logging.FileHandler('hospital.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger