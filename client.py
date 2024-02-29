import asyncio
import aiohttp


async def main():
    client = aiohttp.ClientSession()

    # User

    # response = await client.post(
    #     'http://127.0.0.1:8080/user',
    #     json = {'name':'Dima', 'password': 'Dima_1'},
    # )
    # print('RESPONSE : ctatus _ ', response.status)
    # print(await response.json())

    # response = await client.get('http://127.0.0.1:8080/user/3',)
    # print('RESPONSE : ctatus _ ', response.status)
    # print(await response.json())

    # Advertisement

    response = await client.get('http://127.0.0.1:8080/advertisement/3',)
    print('RESPONSE : ctatus _ ', response.status)
    print(await response.json())

    # response = await client.post(
    #     'http://127.0.0.1:8080/advertisement',
    #     json = {
    #     'title': 'test 11',
    #     'description': 'Test description 11',
    #     'owner': 1
    #     }
    #     )
    # print('RESPONSE : ctatus _ ', response.status)
    # print(await response.json())

    # response = await client.delete('http://127.0.0.1:8080/advertisement/1',)
    # print('RESPONSE : ctatus _ ', response.status)
    # print(await response.json())
   

    await client.close()

   
    
    


asyncio.run(main())
