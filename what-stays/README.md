# What Stays — vertical animated story

Film animasi 3D berdurasi 30 detik tentang kenaikan penghasilan, biaya hidup berulang, kebutuhan, pilihan, dan sisa uang. Sumber narasi: `AUDIO_NARASI_1Y.mp3` yang diberikan pengguna.

[Pratinjau 720p](output/What-Stays-preview-720x1280.mp4?raw=true) · [Unduh Full HD](output/What-Stays-1080x1920.mp4?raw=true) · [Unduh proyek ZIP](output/What-Stays-project.zip?raw=true)

## Hasil

- `output/What-Stays-1080x1920.mp4`: master distribusi, 1080 × 1920, 9:16, 30 fps, H.264, AAC stereo. Caption sudah menyatu dengan gambar.
- `output/What-Stays-preview-720x1280.mp4`: salinan ringan untuk pratinjau.
- `output/What-Stays.en.srt`: caption terpisah untuk penyuntingan.
- `project/`: sumber animasi 3D yang dapat diedit, termasuk geometri, kamera, material, timing, caption, dan audio.
- `assets/alignment.json`: waktu kata yang diperoleh dari forced alignment terhadap audio asli.

Tidak ada musik latar. SFX berupa koin, kertas, langkah ringan, dan perpindahan adegan dibuat secara prosedural. Semua karakter tidak memiliki geometri mulut, sehingga tidak ada lip sync atau animasi berbicara.

## Pratinjau proyek

Jalankan dari direktori ini:

```sh
python -m http.server 8000 --directory project
```

Buka alamat lokal server di browser Anda, lalu tekan **Play with narration**. Proyek menggunakan aset lokal. Tidak memerlukan API, kunci rahasia, layanan AI, atau koneksi ke CDN.

## Render ulang

Prasyarat: Node.js, Playwright, Chromium, Python (NumPy dan SciPy untuk pembuatan ulang SFX), serta FFmpeg.

```sh
npm install
python audio_and_captions.py
node render.cjs
ffmpeg -y -i output/visual-master.mp4 -i project/narration.mp3 -i project/sfx.wav \
  -filter_complex '[1:a]aresample=48000,volume=1.12,apad=whole_dur=30[n];[n][2:a]amix=inputs=2:duration=longest:normalize=0,volume=1.48,alimiter=limit=0.891:level=false:latency=true[a]' \
  -map 0:v:0 -map '[a]' -t 30 -vf 'scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p' \
  -c:v libx264 -preset slow -crf 16 -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart output/What-Stays-1080x1920.mp4
```

`render.cjs` memakai Chromium di `/usr/bin/chromium`; atur variabel `CHROMIUM_PATH` jika lokasi browser berbeda. Variabel `W`, `H`, dan `FPS` mengatur resolusi dan frame rate. `STILLS=1,7.6,15.7,23.5` menghasilkan gambar pemeriksaan tanpa merender seluruh film.

## Keputusan editorial

| Waktu | Visual | Pesan narasi |
|---|---|---|
| 0.00–5.12 | Amplop kenaikan gaji, tumpukan koin tumbuh, sisa dua koin | Penghasilan lebih tinggi belum tentu menghasilkan sisa lebih banyak |
| 5.12–6.82 | Pekerja menerima amplop tambahan penghasilan | Membayangkan kenaikan gaji |
| 6.82–9.15 | Apartemen, furnitur, dan kunci; tanda kenaikan sewa | Memilih apartemen yang lebih mahal |
| 9.15–13.05 | Kalender berganti dan koin menuju pembayaran sewa | Biaya berulang menyerap tambahan pendapatan |
| 13.05–17.48 | Orang tua bersama anak di childcare; tagihan naik | Sebagian kenaikan biaya memenuhi kebutuhan nyata |
| 17.48–19.86 | Sofa lebih mewah dan label biaya per bulan | Sebagian pengeluaran merupakan upgrade opsional |
| 19.86–25.80 | Grafik pemasukan, pengeluaran, dan sisa; buku catatan | Meninjau keduanya bersama untuk mengetahui sisa uang |
| 25.80–30.00 | Karakter mempertimbangkan kenyamanan dan biaya bulanan | Pertanyaan reflektif tentang nilai sebuah upgrade |

Caption mempertahankan teks dan urutan asli, termasuk tanda `[[...]]`. Pemotongan baris hanya untuk keterbacaan. Awal frasa mengikuti penanda waktu audio; beberapa akhir cue diperpanjang ke jeda agar nyaman dibaca. Rasio batang grafik adalah ilustrasi, bukan angka faktual atau rekomendasi anggaran.

Gerak kamera dan karakter dirender pada setiap frame, bukan slideshow gambar diam. Gaya visual: miniatur 3D, palet sage/biru/emas, pencahayaan studio, dan komposisi vertikal. Aset karakter dan properti dibuat dalam kode; tidak memakai model karakter atau video stok.

## Lisensi komponen

Three.js menggunakan lisensi MIT; lihat `project/lib/THREE-LICENSE.txt`. Font DejaVu menggunakan lisensi yang disertakan di `project/lib/DEJAVU-LICENSE.txt`. Hak audio narasi tetap pada pemilik audio. Semua komponen pihak ketiga yang dibundel disertai pemberitahuan lisensinya.
