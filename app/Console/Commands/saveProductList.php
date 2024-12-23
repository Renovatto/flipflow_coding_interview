<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;

use Illuminate\Support\Facades\Http;
use Facebook\WebDriver\Remote\RemoteWebDriver;
use Facebook\WebDriver\Remote\DesiredCapabilities;
use Facebook\WebDriver\WebDriverBy;
use App\Models\Product;

class saveProductList extends Command
{
    protected $signature = 'products:store {url}';
    protected $description = 'store the products';

    public function handle()
    {
        $url = $this->argument('url');
        $this->info("Scraping products from: $url");

        // Caminho para o script Python
        $scriptPath = base_path('scraper.py');

        // Executar o script Python
        $command = escapeshellcmd("python3 $scriptPath " . escapeshellarg($url));
        sleep(5);
        $output = shell_exec($command);

        if ($output === null) {
            $this->error("we have a problem to execute Python script.");
            return 1;
        }

        $this->info("Python script output:");
        $this->line($output);

        $products = json_decode($output, true);

        $this->info("Contagem de produtos: ".count($products));

        if (json_last_error() !== JSON_ERROR_NONE) {
            $this->error('Invalid JSON returned from Python script.');
            return 1;
        }

        foreach ($products as $product) {
            Product::updateOrCreate(
                ['title' => $product['title']],
                [
                    'price' => $product['price'],
                    'image_url' => $product['image'],
                    'product_url' => $product['link'],
                ]
            );
        }

        $this->info('Products stored successfully!');
        return 0;
    }
}
