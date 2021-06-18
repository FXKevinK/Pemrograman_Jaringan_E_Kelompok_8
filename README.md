# Pemrograman_Jaringan_E_Kelompok_8

## Kelompok 8
* 05111840000077 - [Joseph Eric Amadeo Seloatmodjo](https://github.com/josepheric)
* 05111840000081 - [Feinard](https://github.com/feinardslim)
* 05111840000162 - [Fransiskus Xaverius Kevin Koesnadi](https://github.com/fxkevink)

## Daftar Isi
* [Konfigurasi Awal](#konfigurasi-awal)
* [Personal Chat](#personal-chat)
* [Group Chat](#group-chat)
* [Files](#files-message)

## Cara Menjalankan GUI - Tugas Chat

### Konfigurasi Awal 

1. Clone Repository

```git
git clone https://github.com/FXKevinK/Pemrograman_Jaringan_E_Kelompok_8.git
```

2. Arahkan ke direktori hasil *clone* lalu jalankan command berikut

```python
python server_thread_chat.py
```
Dan buka Command Prompt lain utnuk mengaktifkan GUI
```
python chatGUI.py
```

Sehingga jika menjalankan command `python chatGUI.py` sebanyak 3 kali, maka akan memunculkan 3 GUI untuk tiap user yang telah terdaftar

![Img](https://github.com/FXKevinK/Pemrograman_Jaringan_E_Kelompok_8/blob/Tugas_Chat/img/guipolos.png)

## Personal Chat

1. Setelah membuka 2 GUI, masukkan *username* dan *password* ke dalam *entry box* masing-masing GUI dan tekan *button* `Personal Chat`.

![Img](https://github.com/FXKevinK/Pemrograman_Jaringan_E_Kelompok_8/blob/Tugas_Chat/img/gui2.png)


2. Maka akan muncul tampilan untuk memasukkan *message* yang diperlukan. 
* Pada *entry box* pertama masukkan nama tujuan yang akan dikirimkan pesan
* Pada *entry box* kedua masukkan pesan yang akan dikirim. 

    Lakukan hal yang sama pada GUI lain dan tekan tombol *Send*. Maka hasil chat akan muncul pada *chat box*, seperti gambar di bawah.

![Img](https://github.com/FXKevinK/Pemrograman_Jaringan_E_Kelompok_8/blob/Tugas_Chat/img/guipc.png)

## Group Chat

1. Lakukan dengan membuka 2 atau 3 GUI, masukkan *username* dan *password* ke dalam *entry box* masing-masing GUI dan tekan *button* `Group Chat`.

![Img](https://github.com/FXKevinK/Pemrograman_Jaringan_E_Kelompok_8/blob/Tugas_Chat/img/allgui.png)

2. Maka akan muncul tampilan untuk memasukkan *message* yang diperlukan. 
* Pada *entry box* pertama masukkan nama grup yang akan dikirimkan pesan (group1) 
* Pada *entry box* kedua masukkan pesan yang akan dikirim. 

    Lakukan hal yang sama pada GUI lain dan tekan tombol *Send*. Maka hasil chat akan muncul pada *chat box*, seperti gambar di bawah.

![Img](https://github.com/FXKevinK/Pemrograman_Jaringan_E_Kelompok_8/blob/Tugas_Chat/img/guigc.png)


## Files Message

1. Lakukan dengan membuka 2 atau 3 GUI. Bukalah GUI pada folder yang berbeda untuk dapat membuktikan pengiriman file, dalam hal ini folder yang digunakan yaitu `Tugas Chat` dan `temp`, seperti pada gambar berikut.

![Img](https://github.com/FXKevinK/Pemrograman_Jaringan_E_Kelompok_8/blob/Tugas_Chat/img/tugaschatt.png)

![Img](https://github.com/FXKevinK/Pemrograman_Jaringan_E_Kelompok_8/blob/Tugas_Chat/img/tempp.png)

Anggap Folder `Tugas Chat` ber-*username* messi dan `Temp` ber-*username* lineker. Masukkan *username* dan *password* ke dalam *entry box* masing-masing GUI dan tekan *button* `Files`.

![Img](https://github.com/FXKevinK/Pemrograman_Jaringan_E_Kelompok_8/blob/Tugas_Chat/img/guifile.png)

2. Pilih file yang akan dikirimkan ke *user* lain contoh filenya adalah `test1.txt` yang berisikan `hello world`.

![Img](https://github.com/FXKevinK/Pemrograman_Jaringan_E_Kelompok_8/blob/Tugas_Chat/img/heloword1.png)

3. Masukkan di entry box dengan dengan cara:
* Pada *entry box* pertama masukkan nama tujuan yang akan dikirimkan *file*
* Pada *entry box* kedua masukkan pesan yang akan dikirim. 

    Setelah itu pada GUI lain, pilih sumber pengirim pada *dropdown* kiri dan nama file yang dikirimkan pada *dropdown* kanan. Apabila ditemukan, klik *download*.

![Img](https://github.com/FXKevinK/Pemrograman_Jaringan_E_Kelompok_8/blob/Tugas_Chat/img/gui2.png)

5. Hasilnya adalah sebagai berikut

![Img](https://github.com/FXKevinK/Pemrograman_Jaringan_E_Kelompok_8/blob/Tugas_Chat/img/heloword2.png)

