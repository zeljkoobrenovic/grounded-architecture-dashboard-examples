cd data/roadmap
python3 tsv-to-json.py

cd ../..

python3 generate-docs.py
python3 generate-roadmap-docs.py

cd docs/landing_pages
python3 generate-docs.py

cd ../metamorphosis
bash run.sh