<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\Product;

class truncateProducts extends Command
{
    protected $signature = 'products:clear';
    protected $description = 'Truncate products table';

    public function handle()
    {
        Product::truncate();
        $this->info('Success in truncate products table');

        return 0;
    }
}
