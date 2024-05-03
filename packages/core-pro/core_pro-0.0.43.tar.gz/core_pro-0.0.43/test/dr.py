from src.core_pro import Drive
import pandas as pd


# folder = '1YDheK38mWfrdTz6iwFg1lq9M3tMHT123'
# a = Drive().search_files(folder)
#
# df = pd.DataFrame(a)
# for i in ['createdTime', 'modifiedTime']:
#     df[i] = pd.to_datetime(df[i])
#
# latest = df.groupby('name')['createdTime'].max().reset_index()
# latest['latest'] = True
#
# df = df.merge(latest, on=['name', 'createdTime'], how='left')
# df_remove = df.query('latest != latest')
# for i in df_remove.to_dict(orient='records'):
#     Drive().remove_file(i['id'])

# url = '127h31Zzw-mHnE_-vGEWc3ikKhs1MgQAf'
# a = Drive().get_file_info(url)
# url = '1SU-YjuibMc1xO4KzDdVTSlODhLHrFXlx'
# a = Drive().get_file_info(url)

# path = '/home/kevin/Downloads/1.csv'
# folder_id = '1Ez8dNFmLQp936xkQlr1Ke1xW1WgJcvzD'
# drive = Drive()
# file_id = drive.upload(path, 'test.jpg', folder_id=folder_id)
# drive.share_file(file_id, email='xuankhang.do@shopee.com')

# url = '1FseQXxGUyHy4GfVgvvzvDWERhjcctxtsKl2txuVdg7z0QexxZ-PRe8afhvV87AvGJ51PAzzy'
# url = '1t_fKO-N7CrVkhLYkG-Ouu9-Gupc-RiZ8L5ETUWQel9-BMe2EhL6z--H1BXkljAEM8ccqszXN'
# a = Drive().search_files(url)
# b = Drive().remove_file('1N49jLYrhK3rd1TfHKlTgaQQt-QT0fFdk')

# Drive().empty_trash()
