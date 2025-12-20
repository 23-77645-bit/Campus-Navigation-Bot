"""
QR Utility Service
Generates and manages QR codes for water containers and customer management in water refilling station
"""
import qrcode
import uuid
from PIL import Image
import io


class QRUtil:
    @staticmethod
    def generate_unique_qr_code(data: str = None, size: tuple = (200, 200)) -> tuple:
        """
        Generate a unique QR code
        
        Args:
            data (str, optional): Data to encode in the QR code. If None, generates a UUID.
            size (tuple): Size of the QR code image (width, height)
            
        Returns:
            tuple: (qr_code_string, image_bytes) where qr_code_string is the unique identifier
                   and image_bytes is the image data
        """
        if data is None:
            data = str(uuid.uuid4())
        
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Resize if needed
        img = img.resize(size)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()
        
        return data, img_bytes

    @staticmethod
    def save_qr_code_to_file(data: str, filename: str, size: tuple = (200, 200)):
        """
        Save a QR code to a file
        
        Args:
            data (str): Data to encode in the QR code
            filename (str): Path to save the QR code image
            size (tuple): Size of the QR code image (width, height)
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize(size)
        img.save(filename)

    @staticmethod
    def generate_water_container_qr_code(container_id: int, container_type: str) -> str:
        """
        Generate a QR code specifically for a water container
        
        Args:
            container_id (int): ID of the water container
            container_type (str): Type of the water container
            
        Returns:
            str: QR code string identifier
        """
        qr_data = f"WATER_CONTAINER:{container_id}:{container_type}"
        return qr_data

    @staticmethod
    def generate_customer_qr_code(customer_id: int, customer_email: str) -> str:
        """
        Generate a QR code specifically for a customer
        
        Args:
            customer_id (int): ID of the customer
            customer_email (str): Email of the customer
            
        Returns:
            str: QR code string identifier
        """
        qr_data = f"CUSTOMER:{customer_id}:{customer_email}"
        return qr_data

    @staticmethod
    def validate_qr_code(qr_code: str) -> dict:
        """
        Validate and parse a QR code
        
        Args:
            qr_code (str): QR code string to validate
            
        Returns:
            dict: Parsed information from the QR code
        """
        parts = qr_code.split(':')
        
        if len(parts) >= 3:
            entity_type = parts[0]
            entity_id = parts[1]
            
            if entity_type == 'WATER_CONTAINER':
                return {
                    'type': 'water_container',
                    'id': int(entity_id) if entity_id.isdigit() else None,
                    'container_type': ':'.join(parts[2:]) if len(parts) > 2 else None
                }
            elif entity_type == 'CUSTOMER':
                return {
                    'type': 'customer',
                    'id': int(entity_id) if entity_id.isdigit() else None,
                    'email': ':'.join(parts[2:]) if len(parts) > 2 else None
                }
        
        return {
            'type': 'unknown',
            'id': None,
            'data': qr_code
        }