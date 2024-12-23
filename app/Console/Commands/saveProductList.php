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

        // path to python script
        $scriptPath = base_path('scraper.py');

        // execute o python script
        $command = escapeshellcmd("python3 $scriptPath " . escapeshellarg($url));

        //get return scraped products by selenium
        $output = shell_exec($command);

        if ($output === null) {
            $this->error("we have a problem to execute Python script.");
            return 1;
        }

        $this->info("Python script output:");
        $this->line($output);

        $products = json_decode($output, true);

        $this->info("Count products: ".count($products));

        if (json_last_error() !== JSON_ERROR_NONE) {
            $this->error('Invalid JSON returned from python script.');
            return 1;
        }

        // loop to get each product and save in sqLite
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
