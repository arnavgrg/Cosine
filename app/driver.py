from selenium import webdriver

if __name__ == '__main__':
	driver = webdriver.Firefox()
	driver.get("https://demo.docusign.net/Signing/?insession=1&ti=f00f9bbc1f86418b9289e3bf7153526c")