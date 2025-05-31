# Espacio de trabajo, variables locales, Cookies
from time import sleep
import pandas as pd
import numpy as np
from tiktokapipy.async_api import AsyncTikTokAPI

#from TikTokApi import TikTokApi
#csrf_session_id_TikTok = 'verify_lcr1tv3c_3Ymjw5Dz_aaGR_4JMF_BFnC_Qr6c4kkpKa9W'
#api = TikTokApi(custom_verify_fp=csrf_session_id_TikTok)
#user_videos =  api.user(username).info_full()
from tiktokapipy.api import TikTokAPI


#### RECOPILAR MÉTRICAS AL INTERIOR DEL VÍDEO DE UN USUARIO
def recopilar_videos_usuario(n_videos, username):
    df_usuario = pd.DataFrame()
    comments = list()
    with TikTokAPI(navigator_type='firefox', navigation_retries=2, navigation_timeout=10, scroll_down_time=10) as api:
        user = api.user(username, n_videos)
        print(user)
        for video in user.videos:
            num_comments = video.stats.comment_count
            num_likes = video.stats.digg_count
            num_views = video.stats.play_count
            num_shares = video.stats.share_count
            #comments = video.comments
            d = {'num_comments': num_comments, 'num_likes': num_likes, 'num_views': num_views, 'num_shares': num_shares}
            df_usuario = df_usuario.append(d, ignore_index =True)
    return df_usuario
#df_usuario = recopilar_videos_usuario(1, 'elpumajoseluisr')
#print(df_usuario)


### VERSIÓN ASYNC PARA RECOPILAR COMENTARIOS DE UN USUARIO
async def recopilar_comentarios_video_async(video_link):
    async with AsyncTikTokAPI(navigator_type='firefox', navigation_retries=2, navigation_timeout=10, scroll_down_time=10) as api:
        video = await api.video(video_link)
    return await video
#recopilar_comentarios_video_async('https://www.tiktok.com/@lacarito2022/video/7121466607200701701?is_copy_url=1&is_from_webapp=v1&item_id=7121466607200701701&q=%23dariennoticias&t=1664984355496')

### RECOPILAR COMENTARIOS DE UN VIDEO
def recopilar_comentarios_video(video_url):
    with TikTokAPI(navigator_type='firefox', navigation_retries=2, navigation_timeout=10, scroll_down_time=400, headless=True, data_dump_file='dump_try.json') as api:
        video = api.video(video_url)
        comments = video.comments
        print(comments)
        return video.stats
#recopilar_comentarios_video('https://www.tiktok.com/@lacarito2022/video/7121466607200701701')

### RECOPILAR MÉTRICAS DE UN VÍDEO Y DE SU CREADOR
def recopilar_metricas_video_creador(video_url):
    d = dict()
    with TikTokAPI(navigator_type='firefox', navigation_retries=2, navigation_timeout=10, scroll_down_time=10) as api:
        video = api.video(video_url)
        num_comments = video.stats.comment_count
        num_likes = video.stats.digg_count
        num_views = video.stats.play_count
        num_shares = video.stats.share_count
        creator = video.creator()
        followers = creator.stats.follower_count
        following = creator.stats.following_count
        num_videos = creator.stats.video_count
        heart_count = creator.stats.heart_count
        d = {'num_comments': num_comments, 'num_likes': num_likes, 'num_views': num_views, 'num_shares': num_shares,
             'followers': followers, 'following': following, 'num_videos':num_videos, 'heart_count':heart_count}
    return d
# TEST
#recopilar_metricas_video_creador('https://www.tiktok.com/@lacarito2022/video/7121466607200701701')
# Implementación
df_usuarios =  pd.read_excel('Base_feed.xlsx')
df_usuarios['num_comments'] = 0
df_usuarios['num_likes'] = 0
df_usuarios['num_views'] = 0
df_usuarios['num_shares'] = 0
df_usuarios['followers'] = 0
df_usuarios['following'] = 0
df_usuarios['num_videos'] = 0
df_usuarios['heart_count'] = 0
for index, row in df_usuarios.iterrows():
    try:
        video_user_stats = recopilar_metricas_video_creador(row['link'])
        for key in video_user_stats:
            df_usuarios.loc[index,key] = video_user_stats[key]
        print('Recopilé los stats: ' + str(row['usuario']))
        sleep(1)
        df_usuarios.to_excel('Base_feed_con_métricas.xlsx')
    except:
        continue
df_usuarios.to_excel('Base_feed_con_métricas.xlsx')   

