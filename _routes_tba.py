@app.post("/api/user/create", 
    responses={
        201: {"model": schemas.CreateUserResponse},
        401: {
            "model": schemas.HTTPError,
            "description": "Passwords do not match",
        },
        402: {
            "model": schemas.HTTPError,
            "description": "Error sending confirmation email",
        },
        403: {
            "model": schemas.HTTPError,
            "description": "User already exists",
        },
    }, 
    tags=["users"], 
    status_code=201)
async def create_user(payload: schemas.CreateUser, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if user:
         raise HTTPException(status_code=403, detail="User already exists")
    else:
        if payload.password == payload.confirm_password:
            # successful create user (email, hashed pw)
            message, is_valid = helpers.email_is_valid(payload.email)

            if is_valid:
                pw_hash=helpers.generate_password_hash(payload.password)
                db_user = models.User(email=payload.email, 
                                      password_hash=pw_hash,
                                      user_id=helpers.uuid4(),
                                      reset_id=helpers.uuid4(),
                                      create_date=helpers.get_date())

                db.add(db_user)
                db.commit()
                db.refresh(db_user)

                # send email to confirm with a link
                response=schemas.CreateUserResponse(message="Successfully created user; confirm user account via email.",
                                                    user_id=db_user.user_id)
                return response
            else:
                raise HTTPException(status_code=401, detail=message)
        else:
            # passwords do not match
            raise HTTPException(status_code=401, detail="Passwords do not match")

@app.put("/api/user/confirm", 
    responses={
        200: {"model": schemas.UserConfirmResponse},
        404: {
            "model": schemas.HTTPError,
            "description": "User does not exist (from user_id).",
        },
    }, 
    tags=["users"], 
    status_code=200)
async def confirm_user(payload: schemas.UserConfirmPayload, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == payload.user_id, models.User.reset_id == payload.reset_id).first()
    if user:
        user.is_confirmed = True
        user.reset_id = helpers.uuid4()
        db.commit()
        response=schemas.UserConfirmResponse(message="Successfully confirmed user", user_id=user.user_id)
        return response
    else:
        raise HTTPException(status_code=404, detail="User does not exist or reset_id invalid.")

# /api/user/login 
@app.post("/api/user/login", 
    responses={
        200: {"model": schemas.LoginToken},
        401: {
            "model": schemas.HTTPError,
            "description": "Incorrect password for user",
        },
        404: {
            "model": schemas.HTTPError,
            "description": "User does not exist",
        },
    }, 
    tags=["users"], 
    status_code=200)
async def login_user(payload: schemas.LoginUser, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.email ==  payload.email).first()
    if user:
        if helpers.verify_password(user.password_hash, payload.password):
            # create login token (all permissions)
            nowtime=datetime.datetime.now()
            user.last_active = nowtime
            user.login_number = user.login_number + 1
            db.commit()
            db.refresh(api_key)
            db.refresh(user)
            
            login_token=schemas.LoginToken(login_token=api_key.token_id,
                                           expires=api_key.expiration_date)
            return login_token
        else:
            raise HTTPException(status_code=401, detail="Incorrect password for user")
    else:
        raise HTTPException(status_code=404, detail="User does not exist")
