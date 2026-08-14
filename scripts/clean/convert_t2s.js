/**
 * 繁简转换脚本
 * 使用 opencc-js 将繁体诗词数据转换为简体
 * 输入: data/raw/*.json (繁体)
 * 输出: data/interim/*.json (简体)
 */

const fs = require('fs');
const path = require('path');
const { Converter } = require('opencc-js');

// 创建繁体->简体转换器
const converter = Converter({ from: 'tw', to: 'cn' });

function convertText(text) {
  if (typeof text !== 'string') return text;
  return converter(text);
}

function convertArray(arr) {
  if (!Array.isArray(arr)) return arr;
  return arr.map(item => {
    if (typeof item === 'string') return convertText(item);
    return item;
  });
}

function processFile(inputPath, outputPath) {
  const data = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));
  const converted = data.map(item => {
    const result = {};
    for (const [key, value] of Object.entries(item)) {
      if (typeof value === 'string') {
        result[key] = convertText(value);
      } else if (Array.isArray(value)) {
        result[key] = convertArray(value);
      } else {
        result[key] = value;
      }
    }
    return result;
  });
  
  fs.writeFileSync(outputPath, JSON.stringify(converted, null, 2), 'utf-8');
  console.log(`  ${path.basename(inputPath)} -> ${path.basename(outputPath)} (${converted.length} 条)`);
}

function main() {
  const rawDir = path.join(__dirname, '../../data/raw');
  const interimDir = path.join(__dirname, '../../data/interim');
  
  if (!fs.existsSync(interimDir)) {
    fs.mkdirSync(interimDir, { recursive: true });
  }
  
  console.log('=== 繁简转换 ===');
  
  // 转换唐诗
  const tangPath = path.join(rawDir, 'tang_poetry_raw.json');
  if (fs.existsSync(tangPath)) {
    console.log('转换唐诗...');
    processFile(tangPath, path.join(interimDir, 'tang_poetry.json'));
  }
  
  // 转换宋词
  const ciPath = path.join(rawDir, 'song_ci_raw.json');
  if (fs.existsSync(ciPath)) {
    console.log('转换宋词...');
    processFile(ciPath, path.join(interimDir, 'song_ci.json'));
  }
  
  // 转换作者
  const authorsPath = path.join(rawDir, 'authors_raw.json');
  if (fs.existsSync(authorsPath)) {
    console.log('转换作者...');
    processFile(authorsPath, path.join(interimDir, 'authors.json'));
  }
  
  // 复制数据源记录
  const sourcesPath = path.join(rawDir, 'sources.json');
  if (fs.existsSync(sourcesPath)) {
    fs.copyFileSync(sourcesPath, path.join(interimDir, 'sources.json'));
    console.log('复制数据源记录');
  }
  
  console.log('\n繁简转换完成!');
  
  // 验证
  const tangData = JSON.parse(fs.readFileSync(path.join(interimDir, 'tang_poetry.json'), 'utf-8'));
  const ciData = JSON.parse(fs.readFileSync(path.join(interimDir, 'song_ci.json'), 'utf-8'));
  const authorData = JSON.parse(fs.readFileSync(path.join(interimDir, 'authors.json'), 'utf-8'));
  
  console.log(`\n验证:`);
  console.log(`  唐诗: ${tangData.length} 首`);
  console.log(`  宋词: ${ciData.length} 首`);
  console.log(`  作者: ${authorData.length} 位`);
  
  // 检查是否有目标诗人
  const tangAuthors = {};
  tangData.forEach(p => {
    const a = p.author || '';
    tangAuthors[a] = (tangAuthors[a] || 0) + 1;
  });
  
  console.log('\n目标诗人作品数:');
  const targets = ['李白', '杜甫', '王维', '白居易', '孟浩然', '杜牧', '李商隐',
    '王昌龄', '高适', '刘禹锡', '韩愈', '柳宗元', '贾岛', '李贺'];
  targets.forEach(name => {
    console.log(`  ${name}: ${tangAuthors[name] || 0} 首`);
  });
  
  const ciAuthors = {};
  ciData.forEach(p => {
    const a = p.author || '';
    ciAuthors[a] = (ciAuthors[a] || 0) + 1;
  });
  
  const ciTargets = ['苏轼', '辛弃疾', '李清照', '柳永', '陆游', '欧阳修',
    '晏殊', '周邦彦', '姜夔', '秦观', '黄庭坚', '王安石'];
  ciTargets.forEach(name => {
    console.log(`  ${name}: ${ciAuthors[name] || 0} 阕`);
  });
}

main();
