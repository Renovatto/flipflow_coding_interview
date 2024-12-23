const puppeteer = require('puppeteer');

(async () => {
    const url = process.argv[2];
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    // Configurações para simular um navegador
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');

    try {
        // Acesse a URL
        await page.goto(url, { waitUntil: 'networkidle2' });

        // Extrai os dados dos produtos
        const products = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('.product-card')).map(product => ({
                title: product.querySelector('.product-title').innerText.trim(),
                price: product.querySelector('.product-price').innerText.trim(),
                image: product.querySelector('img').src,
                url: product.querySelector('a').href,
            }));
        });

        console.log(JSON.stringify(products.slice(0, 5), null, 2)); // Retorna os primeiros 5 produtos
    } catch (err) {
        console.error('Error fetching products:', err.message);
    }

    await browser.close();
})();
