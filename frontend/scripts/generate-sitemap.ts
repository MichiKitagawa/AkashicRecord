import { writeFileSync } from 'fs';
import { globby } from 'globby';

async function generate() {
  const pages = await globby([
    'src/app/**/page.tsx',
    '!src/app/**/[*',
    '!src/app/api',
  ]);

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      ${pages
        .map((page) => {
          const path = page
            .replace('src/app', '')
            .replace('/page.tsx', '')
            .replace('/index', '');
          return `
            <url>
              <loc>https://your-domain.com${path}</loc>
              <lastmod>${new Date().toISOString()}</lastmod>
              <changefreq>daily</changefreq>
              <priority>0.7</priority>
            </url>
          `;
        })
        .join('')}
    </urlset>
  `;

  writeFileSync('public/sitemap.xml', sitemap);
}

generate(); 