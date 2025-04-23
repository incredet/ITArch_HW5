# ITArch_HW5
0. Install requirements.txt
1. Set up your OpenAI key with command 
    ```
    export OPENAI_KEY=
    ```
2. Set up you token key with command
    ```
    export APP_TOKEN="SuperSecretToken"

    ```
3. Run these three commands in three different terminals

```
fastapi run business_service.py
fastapi run db_service.py --port 8001
fastapi run client_service.py --port 8002

```
4. Run in a separate terminal
```
curl -H "Authorization: Bearer SuperSecretToken" http://localhost:8002/execute
``
5. Boom! Youre super cool openAi user client. Slava Ukraini! I love cats and dogs. <3