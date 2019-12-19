# javac java_build/*.java
# cd java_build
# jar cvf ZipfianGenerator.jar *
# cd ../

# mv java_build/ZipfianGenerator.jar ZipfianGenerator.jar

python3 load_operation_seq.py

cp op_time.csv op_time_full.csv

head -n 400 op_time_full.csv > op_time.csv

python3 lstm.py