rm -f lambda/my-deployment-package.zip
cd lambda/.venv/lib/python3.9/site-packages/
zip -r ../../../../my-deployment-package.zip .
cd ../../../../../
cd lambda/
zip -g my-deployment-package.zip handler.py
cd ../
