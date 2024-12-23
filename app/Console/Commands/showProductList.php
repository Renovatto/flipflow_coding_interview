<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Http;
use App\Models\Product;

class showProductList extends Command
{
    protected $signature = 'products:show {limit=5}';
    protected $description = 'Show products with an optional limit default 5';

    public function handle()
    {
        $limit = (int) $this->argument('limit');

        if ($limit <= 0) {
            $this->error('The limit must be greater than 0.');
            return 1;
        }

        $products = Product::take($limit)->get();

        $this->info($products->toJson(JSON_PRETTY_PRINT));

        return 0;
    }
}
