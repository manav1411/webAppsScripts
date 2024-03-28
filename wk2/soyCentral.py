import jwt

original_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZ3JheW9ucyIsImlzQ2hhZCI6ZmFsc2UsImlhdCI6MTcwODQ5NTgzNn0.LAYJjp9TmGjxEtaolGArgzpbxXUgQnAf2kfN9GdUHrU"
filename = "jwt_secrets.txt"


try:
    with open(filename, "r") as file:
        for secret_to_check in file:
            secret_to_check = secret_to_check.strip()  # Remove any trailing newlines or spaces
            try:
                # Decode the original JWT with the current secret to check its validity.
                # If it's incorrect, it will raise a jwt.exceptions.DecodeError.
                decoded = jwt.decode(original_JWT, secret_to_check, algorithms=["HS256"])
                
                # If the above line did not raise an error, the secret is correct.
                print(f"Found matching secret: {secret_to_check}")
                break
            except jwt.exceptions.DecodeError:
                # This means the secret did not match, and we can continue with the next word.
                continue
            except jwt.exceptions.InvalidTokenError:
                # This means the token is invalid. Raise the exception and exit.
                raise ValueError("The original JWT is invalid")
except FileNotFoundError:
    print(f"File not found: {filename}")


