from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.models.contact_info import ContactInfo
from app.models.family_info import FamilyInfo


class UserService:
    
    @staticmethod
    def get_all_users(db: Session):
        """Get all users with their contact and family info"""
        users = db.query(User).options(
            joinedload(User.family_info),
            joinedload(User.contact_info)
        ).all()
        return users


    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        """Get a user by ID with their contact and family info"""
        user = db.query(User).options(
            joinedload(User.family_info),
            joinedload(User.contact_info)
        ).filter(User.id == user_id).first()
        return user
    
    @staticmethod
    def get_users_simple(db: Session):
        """Get all users without joined data"""
        users = db.query(User).all()
        return users
    
    @staticmethod
    def create_user(user_data: dict, db: Session):
        """Create a new user with family and contact info"""
        # Create user with just the name initially
        db_user = User(name=user_data["name"])
        
        # Get nested data
        family_info_data = user_data.get("family_info", None)
        contact_info_data = user_data.get("contact_info", None)
        
        print(f"Creating user: {user_data}")
        
        # Create and save family_info first
        if family_info_data:
            db_family_info = FamilyInfo(**family_info_data)
            db.add(db_family_info)
            db.commit()
            db.refresh(db_family_info)
            db_user.family_info_id = db_family_info.id

        # Save the user first to get the user ID
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Now create contact_info with the actual user_id
        if contact_info_data:
            contact_info_data["user_id"] = db_user.id  # Add user_id to contact_info
            db_contact_info = ContactInfo(**contact_info_data)
            db.add(db_contact_info)
            db.commit()
            db.refresh(db_contact_info)
            db_user.contact_info_id = db_contact_info.id
            db.commit()  # Update user with contact_info_id
        
        return db_user
    
    @staticmethod
    def update_user(user_id: int, user_data: dict, db: Session):
        """Update an existing user"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None

        # Update user name
        db_user.name = user_data.get("name", db_user.name)
        print(f"Updating user: {db_user}")
        
        # Update family_info if provided
        family_info_data = user_data.get("family_info", None)
        if family_info_data:
            if db_user.family_info:
                for key, value in family_info_data.items():
                    setattr(db_user.family_info, key, value)
            else:
                db_user.family_info = FamilyInfo(**family_info_data)
        
        # Update contact_info if provided
        contact_info_data = user_data.get("contact_info", None)
        if contact_info_data:
            if db_user.contact_info:
                for key, value in contact_info_data.items():
                    setattr(db_user.contact_info, key, value)
            else:
                contact_info_data["user_id"] = db_user.id
                db_user.contact_info = ContactInfo(**contact_info_data)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        print(f"Updated user: {db_user}")
        
        return db_user