from getpass import getpass
import instaloader
import urllib3
import socket
from fileinput import close
import re
import csv
from time import sleep
import os
import sys
import pathlib
from timeit import default_timer as timer
import datetime

import time
import progressbar

from colorama import init
from termcolor import colored
init()


# Get instance
L = instaloader.Instaloader()


def cekkoneksi():
    while True:
        try:
            widgets = ['Cek Internet ..', progressbar.AnimatedMarker()]
            bar = progressbar.ProgressBar(widgets=widgets).start()
            for i in range(20):
                time.sleep(0.1)
                bar.update(i)
            socket.create_connection(('instagram.com', 80))
            os.system('clear')
            os.system('cls' if os.name == 'nt' else 'clear')
            print(colored('Berhasil Terhubung Ke Instagram', 'green'))
            time.sleep(1)
            os.system('clear')
            os.system('cls' if os.name == 'nt' else 'clear')
            return
        except:
            print('Tidak Ada Internet.\n Dimulai kembali dalam 5 detik.\n')
            sleep(5)


def ceklogin():
    ceklogin = 'false'
    while (ceklogin == 'false'):
        print(colored('Terhubung Ke Instagram', 'green'))
        print(
            '--------------------------------------------------------------------------------\n')
        print(
            colored('**-- Aplikasi Scrab Data Followers By Fembi Nur Ilham --**', 'blue'))
        print(
            '--------------------------------------------------------------------------------\n')
        print("Masukkan Akun Instagram Untuk Login")
        print('')

        username = input("Username : ")
        password = getpass("Password : ")

        try:
            print('')
            widgets = ['Mencoba Login ..', progressbar.AnimatedMarker()]
            bar = progressbar.ProgressBar(widgets=widgets).start()
            for i in range(20):
                time.sleep(0.1)
                bar.update(i)

            L.login(username, password)
            ceklogin = 'true'

            time.sleep(5)
            os.system('clear')
            os.system('cls' if os.name == 'nt' else 'clear')
            print(
                colored('Berhasil Login', 'green')
            )
            print(
                '--------------------------------------------------------------------------------\n')
            print(
                colored('**-- Aplikasi Scrab Data Followers By Fembi Nur Ilham --**', 'blue'))
            print(
                '--------------------------------------------------------------------------------\n')
        except:
            os.system('clear')
            os.system('cls' if os.name == 'nt' else 'clear')
            print(colored('Login Tidak Berhasil', 'red'))


def progress(percent=0, width=40):
    left = width * percent // 100
    right = width - left

    tags = "#" * left
    spaces = " " * right
    percents = f"{percent:.0f}%"

    print("\r[", tags, spaces, "]", percents, sep="", end="", flush=True)


def cekakunterakhir(name):
    akunakhir = 'false'
    while (akunakhir == 'false'):
        konfirmasi = input(
            "Lanjutkan Proses Sebelumnya, Ketik 'ya' Untuk Melanjutkan: ")

        if konfirmasi == 'ya':
            try:
                filename = 'downloads/'+name+'.csv'
                dtuser = []
                with open(filename, 'r', newline='', encoding="utf-8") as csvf:
                    file_read = csv.reader(csvf)
                    for row in file_read:
                        dtuser.append(row[1])
                print('Akun Terahir :' + dtuser[-1])
                return dtuser[-1]
            except:
                print('Gagal Mengambil File')
                akunakhir = 'true'
                fileterakhir = ''
                return fileterakhir

        else:
            terakhir = ''
            print('Memulai dari awal')
            return terakhir


cekkoneksi()
ceklogin()

print("Akun Instagram Yang Akan Diambil Followersnya")
akun = input("Akun : ")
print('')
terakhir = cekakunterakhir(akun)
print('--------------------------------------------------------------------------------\n')
time.sleep(5)
os.system('clear')
os.system('cls' if os.name == 'nt' else 'clear')

# Mengambil directory
pathlib.Path('downloads/').mkdir(parents=True, exist_ok=True)
http = urllib3.PoolManager()
start = timer()
curr = str(datetime.datetime.now())

# Akun Scrab
accounts = akun
p = accounts.split('\n')

# Akun Terakhir
last = terakhir
last = last.strip()


for profile in p:
    if last in profile and len(last) > 2:
        print(last, profile)
        p.remove(profile)


print(
    colored('Target : ' + akun, 'white')
)
print(
    '--------------------------------------------------------------------------------\n')
print(
    colored('**-- Aplikasi Scrab Data Followers By Fembi Nur Ilham --**', 'blue'))
print(
    '--------------------------------------------------------------------------------\n')

print('Mengambil Data:', p[0])
PROFILE = p[:]
print(PROFILE)
print('Total Akun Yang Akan Diambil:', len(PROFILE))
print('--------------------------------------------------------------------------------\n')


for ind in range(len(PROFILE)):
    pro = PROFILE[ind]
    try:
        os.system('clear')
        os.system('cls' if os.name == 'nt' else 'clear')
        widgets = ['Mendapatkan Data Follwers Dari '+pro+' ...',
                   progressbar.AnimatedMarker()]
        bar = progressbar.ProgressBar(widgets=widgets).start()
        for i in range(20):
            time.sleep(0.1)
            bar.update(i)

        filename = 'downloads/'+pro+'.csv'
        with open(filename, 'a', newline='', encoding="utf-8") as csvf:

            csv_writer = csv.writer(csvf)
            csv_writer.writerow(['user_id', 'username', 'Nama Lengkap', 'Akun verified', 'Akun private', 'Total Media',
                                'Totol Pengikut', 'Total Mengikuti', 'Bio', 'Website', 'Email', 'Last Activity', 'IGtv_count', 'Akun Bisnis', 'Nama bisnis', 'Foto Profil', 'scrape_of', 'scraped_at'])

        profile = instaloader.Profile.from_username(L.context, pro)
        main_followers = profile.followers
        count = 0
        total = 0

        for person in profile.get_followers():

            dtuser = []
            with open(filename, 'r', newline='', encoding="utf-8") as csvf:
                file_read = csv.reader(csvf)
                for row in file_read:
                    dtuser.append(row[1])
            print(dtuser)

            cek = 'true'
            for cekuser in dtuser:
                if cekuser == person.username:
                    cek = 'false'
                    print(person.username + ' Telah Ada')

            if cek == 'true':
                try:
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

                    igtv_count = person.igtvcount
                    is_business_account = person.is_business_account
                    business_category_name = person.business_category_name
                    profile_pic_url = person.profile_pic_url

                    # last activity
                    try:
                        follower_profile = instaloader.Profile.from_username(
                            L.context, username)
                        for post in follower_profile.get_posts():
                            last_activity = post.date_local
                            break
                    except Exception as e:
                        # print(e)
                        last_activity = ''

                    with open(filename, 'a', newline='', encoding="utf-8") as csvf:
                        csv_writer = csv.writer(csvf)
                        csv_writer.writerow([user_id, username, fullname, is_verified, is_private, media_count,
                                            follower_count, following_count, bio, website, emails, last_activity, igtv_count, is_business_account, business_category_name, profile_pic_url, pro, curr])

                    os.system('clear')
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(
                        colored('Target : ' + akun, 'white')
                    )
                    print(
                        '--------------------------------------------------------------------------------\n')
                    print(
                        colored('**-- Aplikasi Scrab Data Followers By Fembi Nur Ilham --**', 'blue'))
                    print(
                        '--------------------------------------------------------------------------------\n')
                    print('Total akun berhasil diambil:',
                          total, ' dari', main_followers)
                    print('Username:', username)
                    # print('Persen:', round(total/main_followers*100), '%')
                    print('Waktu:', str(datetime.timedelta(
                        seconds=(round(timer()-start)))))
                    # print('Current Account:', ind+1, '\t Remaining Accounts:', len(PROFILE)-ind-1, '\nAccount Name:', pro)

                    progress(round(total/main_followers*100))

                except Exception as e:
                    print(e)

        # (likewise with profile.get_followers())
    except:
        print('Skipping', pro)
