from app.errors.bookbnb_error import EmailAlreadyInUseError
from app.errors.http_error import NotFoundError
from app.model.registered_user import RegisteredUser


class RegisteredUserDAO:
    @classmethod
    def add_new_registered_user(cls, db, registered_user_args):
        email = registered_user_args.email

        existent_user = (
            db.query(RegisteredUser)
            .filter(RegisteredUser.email == registered_user_args.email.lower())
            .first()
        )

        if existent_user is not None:
            raise EmailAlreadyInUseError(email)

        new_registerd_user = RegisteredUser(email=registered_user_args.email.lower())

        db.add(new_registerd_user)
        db.commit()

        return new_registerd_user.serialize()

    @classmethod
    def get_by_email(cls, db, email):
        registerd_user = (
            db.query(RegisteredUser).filter(RegisteredUser.email == email).first()
        )

        if registerd_user is None:
            raise NotFoundError("User")

        return registerd_user.serialize()
    
    @classmethod
    def delete_by_uuid(cls, db, uuid):
        registerd_user = db.query(RegisteredUser).get(uuid)

        if registerd_user is None:
            raise NotFoundError("User")
        
        db.delete(registerd_user)
        db.commit()

        return registerd_user.serialize()
