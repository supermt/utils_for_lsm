for i in {0..1000..1}
do 
	./ldb --db=/tmp/test_db --create_if_missing put a1 b1
done
