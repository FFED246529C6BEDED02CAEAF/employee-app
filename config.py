# Import necessary libraries
import os

# Application configuration class
class Config:
    # Base configuration for all environments
    DEBUG = False  # Set to True for development mode
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')  # Use secure environment variable
    SQLALCHEMY_DATABASE_URI = 'sqlite:///employee_portal.db'  # Change for your database connection string

    # Define environment-specific configurations
    @classmethod
    def from_object(cls, env_name):
        # Import environment-specific configurations
        env_config = __import__(f"config.{env_name}", fromlist=['Config'])
        return env_config.Config

# Choose the current environment configuration
app_config = Config.from_object(os.environ.get('FLASK_ENV', 'development'))
