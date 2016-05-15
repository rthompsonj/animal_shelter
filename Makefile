build:
	docker build -t shelter .
run:
	docker run -itd -p 5000:5000 --name=SHELTER shelter
