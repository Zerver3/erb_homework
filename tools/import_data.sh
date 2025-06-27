cd tools

rm -rf data
rm -rf photo

# delete all dbs
python clean_db.py

python collect_books.py
python process_books.py
python add_books.py

rm -rf data
