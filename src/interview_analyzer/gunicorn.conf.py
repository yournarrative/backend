import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1

# see: https://gist.github.com/HacKanCuBa/275bfca09d614ee9370727f5f40dab9e
