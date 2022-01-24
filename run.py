from fileinput import close
import re
import csv
from time import sleep
import os
import sys
import pathlib
from timeit import default_timer as timer
import datetime


import urllib3
import instaloader

# Get instance
L = instaloader.Instaloader()

# Login or load session


print('--------------------------------------------------------------------------------\n')
print("Masukkan Akun Instagram Untuk Login")
username = input("Username : ")
password = input("Password : ")

try:
    print('Mencoba Login...')
    L.login(username, password)
    print('Berhasil Login...')
except:
    print('Gagal Login!')
    print('--------------------------------------------------------------------------------\n')
    print('Masukkan Kembali Akun Instagram!')
    username = input("Username : ")
    password = input("Password : ")
    try:
        print('Mencoba Login...')
        L.login(username, password)
        print('Berhasil Login...')
    except:
        print('Gagal Login! Jalankan Kembali')
        print('--------------------------------------------------------------------------------\n')
        sys.exit()

print('--------------------------------------------------------------------------------\n')
print("Akun Instagram Yang Akan Diambil Followersnya")
akun = input("Akun : ")
print("Akun Instagram Yang Terakhir Di Excel (Kosongkan untuk dimulai dari awal)")
terakhir = input("Akun Akhir: ")
print('--------------------------------------------------------------------------------\n')

pathlib.Path('downloads/').mkdir(parents=True, exist_ok=True)

http = urllib3.PoolManager()


start = timer()
curr = str(datetime.datetime.now())


def wait_for_internet_connection():
    while True:
        try:

            response = http.request('GET', 'http://ku.edu.np')
            return
        except:
            print('No internet connection.\nTrying after 5 seconds.\n')
            sleep(5)


# wait_for_internet_connection()


# f = open('input.txt', 'r')
# accounts = f.read()
accounts = akun
p = accounts.split('\n')


# with open('last.txt', 'r') as f:
#     last = f.read()
last = terakhir
last = last.strip()
print('Akun terakhir excel:', last)

for profile in p:
    if last in profile and len(last) > 2:
        print(last, profile)
        p.remove(profile)


# input()
print('Mengambil Data:', p[0])
PROFILE = p[:]
print(PROFILE)
print('Total Akun Yang Akan Diambil:', len(PROFILE))
print('--------------------------------------------------------------------------------\n')

for ind in range(len(PROFILE)):
    pro = PROFILE[ind]
    try:
        #         wait_for_internet_connection()
        print('Mendapatkan Data Follwers Dari', pro)
        filename = 'downloads/'+pro+'.csv'
        with open(filename, 'a', newline='', encoding="utf-8") as csvf:

            csv_writer = csv.writer(csvf)
            csv_writer.writerow(['user_id', 'username', 'fullname', 'is_verified', 'is_private', 'media_count',
                                'follower_count', 'following_count', 'bio', 'website', 'emails', 'last_activity', 'scrape_of', 'scraped_at'])

        profile = instaloader.Profile.from_username(L.context, pro)
        main_followers = profile.followers
        count = 0
        total = 0
        # Print list of followees
        for person in profile.get_followers():
            try:
             #                 wait_for_internet_connection()
                total += 1
                user_id = person.userid
                username = person.username
                fullname = person.full_name
                is_verified = person.is_verified
                is_private = person.is_private
                media_count = person.mediacount
                follower_count = person.followers
                following_count = person.followees
                bio = person.biography
                emails = re.findall(
                    r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", bio)
                website = person.external_url
                # last activity
                try:
                    follower_profile = instaloader.Profile.from_username(
                        L.context, username)
                    for post in follower_profile.get_posts():
                        last_activity = post.date_local
                        break
                except Exception as e:
                    print(e)
                    last_activity = ''

                print('Username:', username)
                print('Last Activity', last_activity)
                with open(filename, 'a', newline='', encoding="utf-8") as csvf:

                    csv_writer = csv.writer(csvf)
                    csv_writer.writerow([user_id, username, fullname, is_verified, is_private, media_count,
                                        follower_count, following_count, bio, website, emails, last_activity, pro, curr])

                # os.system('clear')
                # os.system('cls' if os.name == 'nt' else 'clear')

                print('--------------------------------------------------------------------------------\nTotal akun berhasil diambil:',
                      total, ' dari', main_followers)
                print('Persentase:', total/main_followers*100, '%')
                print('Time:', str(datetime.timedelta(seconds=(timer()-start))))
                print('Current Account:', ind+1, '\t Remaining Accounts:',
                      len(PROFILE)-ind-1, '\nAccount Name:', pro)

            except Exception as e:
                print(e)

        # saving the last account for resume
        # f = open('last.txt', 'w+')
        # f.write(pro)
        # f.close()
        # log of completed account
        # f = open('completed.txt', 'a+')
        # f.write(pro+'\n')
        # f.close()
        # (likewise with profile.get_followers())
    except:
        print('Skipping', pro)
