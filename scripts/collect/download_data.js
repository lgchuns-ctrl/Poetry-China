/**
 * 数据采集脚本 - 使用 Node.js https 下载唐诗宋词
 * 数据源: chinese-poetry GitHub 仓库 (MIT License)
 */
const https = require('https');
const fs = require('fs');
const path = require('path');

const RAW_DIR = path.join(__dirname, '../../data/raw');
const BASE = 'https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/';

function fetchJSON(urlPath) {
  return new Promise((resolve, reject) => {
    const encoded = encodeURI(urlPath);
    const url = BASE + encoded;
    
    const req = https.get(url, {
      headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' },
      timeout: 120000
    }, (res) => {
      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}`));
        return;
      }
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch(e) {
          reject(new Error(`JSON parse error: ${e.message}`));
        }
      });
    });
    
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    
    req.on('error', reject);
  });
}

async function downloadWithRetry(urlPath, retries = 5) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fetchJSON(urlPath);
    } catch(e) {
      console.log(`  Retry ${i+1}/${retries}: ${e.message}`);
      if (i < retries - 1) await new Promise(r => setTimeout(r, 3000));
    }
  }
  throw new Error('Max retries reached');
}

async function main() {
  console.log('========================================');
  console.log('《诗行中国》数据采集 (Node.js)');
  console.log('========================================\n');
  
  // 下载唐诗
  console.log('=== 下载唐诗 ===');
  let allTang = [];
  for (let i = 0; i <= 14000; i += 1000) {
    const filename = `poet.tang.${i}.json`;
    console.log(`  下载 ${filename}...`, end = ' ');
    try {
      const data = await downloadWithRetry(`全唐诗/${filename}`);
      allTang = allTang.concat(data);
      console.log(`OK (${data.length} 首), 累计 ${allTang.length}`);
    } catch(e) {
      console.log(`FAIL: ${e.message}`);
      break;
    }
    await new Promise(r => setTimeout(r, 1000));
  }
  console.log(`唐诗总计: ${allTang.length} 首\n`);
  
  // 下载宋词
  console.log('=== 下载宋词 ===');
  let allCi = [];
  for (let i = 0; i <= 5000; i += 1000) {
    const filename = `ci.song.${i}.json`;
    console.log(`  下载 ${filename}...`, end = ' ');
    try {
      const data = await downloadWithRetry(`宋词/${filename}`);
      allCi = allCi.concat(data);
      console.log(`OK (${data.length} 首), 累计 ${allCi.length}`);
    } catch(e) {
      console.log(`FAIL: ${e.message}`);
      break;
    }
    await new Promise(r => setTimeout(r, 1000));
  }
  console.log(`宋词总计: ${allCi.length} 首\n`);
  
  // 保存
  if (!fs.existsSync(RAW_DIR)) fs.mkdirSync(RAW_DIR, { recursive: true });
  
  fs.writeFileSync(
    path.join(RAW_DIR, 'tang_poetry_raw.json'),
    JSON.stringify(allTang, null, 2), 'utf-8'
  );
  console.log(`保存唐诗: ${allTang.length} 首`);
  
  fs.writeFileSync(
    path.join(RAW_DIR, 'song_ci_raw.json'),
    JSON.stringify(allCi, null, 2), 'utf-8'
  );
  console.log(`保存宋词: ${allCi.length} 首`);
  
  // 统计
  console.log('\n=== 诗人作品统计 ===');
  
  // 唐诗作者统计
  const tangAuthors = {};
  allTang.forEach(p => {
    const a = p.author || '';
    if (!tangAuthors[a]) tangAuthors[a] = 0;
    tangAuthors[a]++;
  });
  
  const tangTargets = ['李白', '杜甫', '王维', '白居易', '孟浩然', '杜牧', '李商隐',
    '王昌龄', '高适', '刘禹锡', '韩愈', '柳宗元', '贾岛', '李贺'];
  console.log('唐诗:');
  tangTargets.forEach(name => {
    console.log(`  ${name}: ${tangAuthors[name] || 0} 首`);
  });
  
  // 宋词作者统计
  const ciAuthors = {};
  allCi.forEach(p => {
    const a = p.author || '';
    if (!ciAuthors[a]) ciAuthors[a] = 0;
    ciAuthors[a]++;
  });
  
  const ciTargets = ['苏轼', '辛弃疾', '李清照', '柳永', '陆游', '欧阳修',
    '晏殊', '周邦彦', '姜夔', '秦观', '黄庭坚', '王安石'];
  console.log('宋词:');
  ciTargets.forEach(name => {
    console.log(`  ${name}: ${ciAuthors[name] || 0} 首`);
  });
}

main().catch(console.error);
