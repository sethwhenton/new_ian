#!/usr/bin/python3
"""
Database Configuration for Production Deployment
"""
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from .config import config

class DatabaseConfig:
    """Database configuration and connection management"""
    
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self.setup_database()
    
    def setup_database(self):
        """Setup database connection based on configuration"""
        try:
            if config.DATABASE_TYPE == 'mysql':
                self._setup_mysql()
            elif config.DATABASE_TYPE == 'postgresql':
                self._setup_postgresql()
            else:
                self._setup_sqlite()
            
            logging.info(f"Database connection established: {config.DATABASE_TYPE}")
            
        except Exception as e:
            logging.error(f"Failed to setup database: {e}")
            raise
    
    def _setup_mysql(self):
        """Setup MySQL database connection"""
        database_url = config.get_database_url()
        
        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=config.DEBUG
        )
        
        self.session_factory = scoped_session(
            sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        )
    
    def _setup_postgresql(self):
        """Setup PostgreSQL database connection"""
        database_url = config.get_database_url()
        
        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=config.DEBUG
        )
        
        self.session_factory = scoped_session(
            sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        )
    
    def _setup_sqlite(self):
        """Setup SQLite database connection"""
        database_url = f"sqlite:///{config.DATABASE_PATH}"
        
        self.engine = create_engine(
            database_url,
            echo=config.DEBUG,
            connect_args={"check_same_thread": False}
        )
        
        self.session_factory = scoped_session(
            sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        )
    
    def get_session(self):
        """Get database session"""
        return self.session_factory()
    
    def create_tables(self):
        """Create all database tables"""
        try:
            from .storage.base_model import Base
            Base.metadata.create_all(self.engine)
            logging.info("Database tables created successfully")
        except Exception as e:
            logging.error(f"Failed to create database tables: {e}")
            raise
    
    def close_connections(self):
        """Close all database connections"""
        if self.session_factory:
            self.session_factory.remove()
        if self.engine:
            self.engine.dispose()
        logging.info("Database connections closed")

# Global database instance
db_config = DatabaseConfig()



