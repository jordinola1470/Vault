import asyncio
import os
import pandas as pd
import datetime
from TikTokApi import TikTokApi



ms_token = os.getenv("verify_lvb8jjct_hXTIR2fu_BwUC_4x8N_9LKb_qretHzatA3q4", None) # get your own ms_token from your cookies on tiktok.com

async def get_video_stats(url):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video = api.video(
            url=url
        )

        video_info = await video.info()  # is HTML request, so avoid using this too much

        stats = video_info.get('stats')
        num_comments = video.stats.get('commentCount')
        num_likes = video.stats.get('diggCount')
        num_views = video.stats.get('playCount')
        num_shares = video.stats.get('shareCount')

        author = video_info.get('author')
        user_name = author['uniqueId']

        desc = video_info.get("desc")

        createDate = int(video_info.get("createTime"))
        date = str(datetime.datetime.utcfromtimestamp(createDate))
        

    return {'UserName': user_name,
            'Description':desc,
            'Date': date,
            'URL': url,
            'Comments': num_comments,
            'Likes': num_likes,
            'Views': num_views,
            'Shares': num_shares
        }



async def main():
    # Leer URLs desde el archivo de Excel
    df = pd.read_excel(r'columbia\videos_columbia.xlsx')
    urls = df['link'].tolist()
    base_final = pd.DataFrame()

    # Recopilar estadísticas para cada URL
    for i, url in enumerate(urls, start=1):
        print(f'Procesando URL {i} de {len(urls)}: {url}')
        try:
            result = await get_video_stats(url)
            print(f'  - Completado para URL: {url}')
        except Exception as e:
            print(f'  - Error al procesar URL {url}: {e}')
            continue

    # Crear un DataFrame con los resultados y almacenarlo en un nuevo archivo de Excel
        base_temporal = pd.DataFrame(data=result,index=[i])
        base_final = pd.concat([base_final, base_temporal], ignore_index=True)

    base_final.to_excel(r'columbia\videos_columbia_metricas.xlsx')


if __name__ == "__main__":
    asyncio.run(main())




    