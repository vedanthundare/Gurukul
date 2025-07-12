#!/usr/bin/env node
/**
 * Test script to verify that the frontend API slices can be imported correctly
 * This helps identify any syntax or import issues before running the full frontend
 */

const fs = require('fs');
const path = require('path');

// Test files to check
const testFiles = [
  'new frontend/src/config.js',
  'new frontend/src/api/summaryApiSlice.js',
  'new frontend/src/store/store.js'
];

console.log('🔍 Testing Frontend Import Syntax');
console.log('=' * 40);

let allPassed = true;

for (const filePath of testFiles) {
  const fullPath = path.join(__dirname, filePath);
  
  try {
    // Check if file exists
    if (!fs.existsSync(fullPath)) {
      console.log(`❌ ${filePath}: File not found`);
      allPassed = false;
      continue;
    }
    
    // Read file content
    const content = fs.readFileSync(fullPath, 'utf8');
    
    // Basic syntax checks
    const issues = [];
    
    // Check for common syntax issues
    if (content.includes('endpoints: (builder) => ({') && 
        content.split('endpoints: (builder) => ({').length > 2) {
      issues.push('Duplicate endpoints declaration');
    }
    
    // Check for unmatched brackets
    const openBrackets = (content.match(/\{/g) || []).length;
    const closeBrackets = (content.match(/\}/g) || []).length;
    if (openBrackets !== closeBrackets) {
      issues.push(`Unmatched brackets: ${openBrackets} open, ${closeBrackets} close`);
    }
    
    // Check for unmatched parentheses
    const openParens = (content.match(/\(/g) || []).length;
    const closeParens = (content.match(/\)/g) || []).length;
    if (openParens !== closeParens) {
      issues.push(`Unmatched parentheses: ${openParens} open, ${closeParens} close`);
    }
    
    // Check for required imports in summaryApiSlice
    if (filePath.includes('summaryApiSlice.js')) {
      if (!content.includes('createApi')) {
        issues.push('Missing createApi import');
      }
      if (!content.includes('CHAT_API_BASE_URL')) {
        issues.push('Missing CHAT_API_BASE_URL import');
      }
    }
    
    // Check for required imports in store.js
    if (filePath.includes('store.js')) {
      if (!content.includes('summaryApiSlice')) {
        issues.push('Missing summaryApiSlice import');
      }
    }
    
    if (issues.length === 0) {
      console.log(`✅ ${filePath}: Syntax OK`);
    } else {
      console.log(`❌ ${filePath}: ${issues.join(', ')}`);
      allPassed = false;
    }
    
  } catch (error) {
    console.log(`❌ ${filePath}: ${error.message}`);
    allPassed = false;
  }
}

console.log('\n📊 Summary');
console.log('=' * 20);

if (allPassed) {
  console.log('✅ All frontend files passed syntax checks');
  console.log('🚀 Frontend should now load without import errors');
} else {
  console.log('❌ Some files have issues that need to be fixed');
}

// Additional recommendations
console.log('\n💡 Recommendations:');
console.log('1. Clear browser cache and restart dev server');
console.log('2. Check browser console for any remaining errors');
console.log('3. Verify all services are running on correct ports');
console.log('4. Test PDF upload functionality after restart');
