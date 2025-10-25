// IME辞書管理ツール JavaScript

let dictionaryData = {
    "辞書情報": {
        "名前": "新しい辞書",
        "説明": "",
        "更新日": new Date().toISOString().split('T')[0]
    },
    "カテゴリ": {}
};

let currentCategory = null;
let editingWordIndex = -1;

// ファイル読み込み処理
document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            dictionaryData = JSON.parse(e.target.result);
            updateUI();
            showNotification('✅ ファイルを読み込みました', 'success');
        } catch (error) {
            showNotification('❌ ファイルの読み込みに失敗しました: ' + error.message, 'error');
        }
    };
    reader.readAsText(file);
});

// UI更新
function updateUI() {
    updateStats();
    updateCategoryList();
    updateWordList();
    updateExportCategorySelection();
}

// 統計情報更新
function updateStats() {
    const categories = Object.keys(dictionaryData.カテゴリ || {});
    const totalWords = categories.reduce((sum, cat) => {
        return sum + (dictionaryData.カテゴリ[cat].単語リスト?.length || 0);
    }, 0);

    const activeWords = categories.reduce((sum, cat) => {
        if (dictionaryData.カテゴリ[cat].有効 === false) return sum;
        return sum + (dictionaryData.カテゴリ[cat].単語リスト?.length || 0);
    }, 0);

    document.getElementById('totalCategories').textContent = categories.length;
    document.getElementById('totalWords').textContent = totalWords;
    document.getElementById('activeWords').textContent = activeWords;
}

// カテゴリリスト更新
function updateCategoryList() {
    const container = document.getElementById('categoryList');
    container.innerHTML = '';

    Object.keys(dictionaryData.カテゴリ || {}).forEach(categoryKey => {
        const category = dictionaryData.カテゴリ[categoryKey];
        const div = document.createElement('div');
        div.className = 'category-item';
        if (categoryKey === currentCategory) {
            div.classList.add('active');
        }

        div.innerHTML = `
            <div class="category-name">${categoryKey}</div>
            <div class="category-description">${category.説明 || ''}</div>
            <div class="category-description">単語数: ${category.単語リスト?.length || 0}</div>
        `;

        div.onclick = () => selectCategory(categoryKey);
        container.appendChild(div);
    });
}

// 単語リスト更新
function updateWordList() {
    const container = document.getElementById('wordList');
    container.innerHTML = '';

    if (!currentCategory || !dictionaryData.カテゴリ[currentCategory]) {
        container.innerHTML = '<p>カテゴリを選択してください</p>';
        return;
    }

    const words = dictionaryData.カテゴリ[currentCategory].単語リスト || [];
    const searchTerm = document.getElementById('searchBox').value.toLowerCase();

    const filteredWords = words.filter(word => {
        return word.読み.toLowerCase().includes(searchTerm) ||
               word.単語.toLowerCase().includes(searchTerm) ||
               (word.説明 && word.説明.toLowerCase().includes(searchTerm));
    });

    if (filteredWords.length === 0) {
        container.innerHTML = '<p>単語が見つかりません</p>';
        return;
    }

    filteredWords.forEach((word, index) => {
        const div = document.createElement('div');
        div.className = 'word-item';

        const tags = word.タグ ? word.タグ.join(', ') : '';

        div.innerHTML = `
            <div>
                <div class="word-reading">${word.読み}</div>
                <div class="word-meta">${word.品詞 || '名詞'}</div>
            </div>
            <div>
                <div class="word-text">${word.単語}</div>
                <div class="word-meta">${word.説明 || ''}</div>
            </div>
            <div class="word-meta">${tags}</div>
            <div>
                <button onclick="editWord(${words.indexOf(word)})" class="btn-primary" style="margin-right: 5px;">編集</button>
                <button onclick="deleteWord(${words.indexOf(word)})" class="btn-danger">削除</button>
            </div>
        `;

        container.appendChild(div);
    });
}

// カテゴリ選択
function selectCategory(categoryKey) {
    currentCategory = categoryKey;
    updateCategoryList();
    updateWordList();
}

// 検索機能
function filterWords() {
    updateWordList();
}

// 通知表示
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : '#3498db'};
        color: white;
        border-radius: 5px;
        z-index: 10000;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// JSONファイル保存
function saveJSON() {
    dictionaryData.辞書情報.更新日 = new Date().toISOString().split('T')[0];

    const dataStr = JSON.stringify(dictionaryData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});

    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = 'dictionary.json';
    link.click();

    showNotification('💾 JSONファイルを保存しました', 'success');
}

// 単語追加モーダル
function openAddWordModal() {
    if (Object.keys(dictionaryData.カテゴリ).length === 0) {
        showNotification('⚠️ 先にカテゴリを作成してください', 'error');
        return;
    }

    document.getElementById('wordModalTitle').textContent = '単語を追加';
    document.getElementById('wordForm').reset();
    updateCategoryOptions();
    document.getElementById('wordCategory').value = currentCategory || Object.keys(dictionaryData.カテゴリ)[0];
    editingWordIndex = -1;
    document.getElementById('wordModal').style.display = 'block';
}

function closeWordModal() {
    document.getElementById('wordModal').style.display = 'none';
}

// 単語編集
function editWord(index) {
    if (!currentCategory || !dictionaryData.カテゴリ[currentCategory]) return;

    const word = dictionaryData.カテゴリ[currentCategory].単語リスト[index];

    document.getElementById('wordModalTitle').textContent = '単語を編集';
    document.getElementById('wordReading').value = word.読み;
    document.getElementById('wordText').value = word.単語;
    document.getElementById('wordPOS').value = word.品詞 || '名詞';
    document.getElementById('wordDescription').value = word.説明 || '';
    document.getElementById('wordTags').value = word.タグ ? word.タグ.join(', ') : '';

    updateCategoryOptions();
    document.getElementById('wordCategory').value = currentCategory;

    editingWordIndex = index;
    document.getElementById('wordModal').style.display = 'block';
}

// 単語削除
function deleteWord(index) {
    if (!currentCategory || !dictionaryData.カテゴリ[currentCategory]) return;

    if (confirm('この単語を削除しますか？')) {
        dictionaryData.カテゴリ[currentCategory].単語リスト.splice(index, 1);
        updateUI();
        showNotification('🗑️ 単語を削除しました', 'success');
    }
}

// 単語フォーム送信
document.getElementById('wordForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const reading = document.getElementById('wordReading').value.trim();
    const word = document.getElementById('wordText').value.trim();
    const pos = document.getElementById('wordPOS').value;
    const description = document.getElementById('wordDescription').value.trim();
    const tagsStr = document.getElementById('wordTags').value.trim();
    const categoryKey = document.getElementById('wordCategory').value;

    if (!reading || !word) {
        showNotification('⚠️ 読みと単語は必須です', 'error');
        return;
    }

    const tags = tagsStr ? tagsStr.split(',').map(tag => tag.trim()).filter(tag => tag) : [];

    const wordData = {
        読み: reading,
        単語: word,
        品詞: pos,
        説明: description,
        タグ: tags
    };

    if (!dictionaryData.カテゴリ[categoryKey].単語リスト) {
        dictionaryData.カテゴリ[categoryKey].単語リスト = [];
    }

    if (editingWordIndex >= 0) {
        // 編集モード
        if (categoryKey !== currentCategory) {
            // カテゴリ変更の場合
            dictionaryData.カテゴリ[currentCategory].単語リスト.splice(editingWordIndex, 1);
            dictionaryData.カテゴリ[categoryKey].単語リスト.push(wordData);
            currentCategory = categoryKey;
        } else {
            dictionaryData.カテゴリ[categoryKey].単語リスト[editingWordIndex] = wordData;
        }
        showNotification('✏️ 単語を更新しました', 'success');
    } else {
        // 新規追加
        dictionaryData.カテゴリ[categoryKey].単語リスト.push(wordData);
        currentCategory = categoryKey;
        showNotification('➕ 単語を追加しました', 'success');
    }

    closeWordModal();
    updateUI();
});

// カテゴリ追加モーダル
function openAddCategoryModal() {
    document.getElementById('categoryForm').reset();
    document.getElementById('categoryModal').style.display = 'block';
}

function closeCategoryModal() {
    document.getElementById('categoryModal').style.display = 'none';
}

// カテゴリフォーム送信
document.getElementById('categoryForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const name = document.getElementById('categoryName').value.trim();
    const description = document.getElementById('categoryDescription').value.trim();

    if (!name) {
        showNotification('⚠️ カテゴリ名は必須です', 'error');
        return;
    }

    if (dictionaryData.カテゴリ[name]) {
        showNotification('⚠️ 同じ名前のカテゴリが既に存在します', 'error');
        return;
    }

    dictionaryData.カテゴリ[name] = {
        説明: description,
        有効: true,
        単語リスト: []
    };

    currentCategory = name;
    closeCategoryModal();
    updateUI();
    showNotification('📁 カテゴリを追加しました', 'success');
});

// カテゴリオプション更新
function updateCategoryOptions() {
    const select = document.getElementById('wordCategory');
    select.innerHTML = '';

    Object.keys(dictionaryData.カテゴリ).forEach(categoryKey => {
        const option = document.createElement('option');
        option.value = categoryKey;
        option.textContent = categoryKey;
        select.appendChild(option);
    });
}

// エクスポート用カテゴリ選択UI更新
function updateExportCategorySelection() {
    const container = document.getElementById('exportCategorySelection');
    container.innerHTML = '';

    const categories = Object.keys(dictionaryData.カテゴリ || {});

    if (categories.length === 0) {
        container.innerHTML = '<p style="color: #999; text-align: center;">カテゴリがありません</p>';
        return;
    }

    categories.forEach(categoryKey => {
        const category = dictionaryData.カテゴリ[categoryKey];
        const wordCount = category.単語リスト?.length || 0;

        const label = document.createElement('label');
        label.style.cssText = 'display: block; padding: 8px; cursor: pointer; border-bottom: 1px solid #eee;';
        label.innerHTML = `
            <input type="checkbox" class="export-category-checkbox" value="${categoryKey}" checked style="margin-right: 10px;">
            <strong>${categoryKey}</strong> <span style="color: #666; font-size: 12px;">(${wordCount}件)</span>
            ${category.説明 ? `<span style="color: #999; font-size: 12px; display: block; margin-left: 24px;">${category.説明}</span>` : ''}
        `;

        container.appendChild(label);
    });
}

// 全カテゴリ選択
function selectAllCategories() {
    document.querySelectorAll('.export-category-checkbox').forEach(checkbox => {
        checkbox.checked = true;
    });
}

// 全カテゴリ選択解除
function deselectAllCategories() {
    document.querySelectorAll('.export-category-checkbox').forEach(checkbox => {
        checkbox.checked = false;
    });
}

// 選択されたカテゴリを取得
function getSelectedCategories() {
    const checkboxes = document.querySelectorAll('.export-category-checkbox:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

// CSVフィールドのエスケープ（ダブルクォートを2重にする）
function escapeCSVField(field) {
    if (field == null) return '';
    const str = String(field);
    // ダブルクォートを2重にしてエスケープ
    return str.replace(/"/g, '""');
}

// エクスポート機能
function exportToCSV() {
    const selectedCategories = getSelectedCategories();
    if (selectedCategories.length === 0) {
        showNotification('⚠️ エクスポートするカテゴリを選択してください', 'error');
        return;
    }

    const data = getCurrentCategoryData(selectedCategories);
    if (!data.length) {
        showNotification('⚠️ エクスポートするデータがありません', 'error');
        return;
    }

    // CSVヘッダー行
    const header = '"読み","単語","品詞","説明","タグ","カテゴリ"';

    // データ行
    const rows = data.map(word => {
        const tags = word.タグ ? word.タグ.join(';') : '';
        return [
            escapeCSVField(word.読み),
            escapeCSVField(word.単語),
            escapeCSVField(word.品詞 || '名詞'),
            escapeCSVField(word.説明 || ''),
            escapeCSVField(tags),
            escapeCSVField(word.カテゴリ || '')
        ].map(field => `"${field}"`).join(',');
    });

    // BOM + ヘッダー + データ
    const csvContent = '\uFEFF' + [header, ...rows].join('\n');

    downloadFile(csvContent, 'dictionary.csv', 'text/csv');
    showNotification(`📄 CSV形式で出力しました (${selectedCategories.length}カテゴリ, ${data.length}件)`, 'success');
}

function exportToTXT() {
    const selectedCategories = getSelectedCategories();
    if (selectedCategories.length === 0) {
        showNotification('⚠️ エクスポートするカテゴリを選択してください', 'error');
        return;
    }

    const data = getCurrentCategoryData(selectedCategories);
    if (!data.length) {
        showNotification('⚠️ エクスポートするデータがありません', 'error');
        return;
    }

    const txtContent = data.map(word => {
        return `${word.読み}\t${word.単語}\t${word.品詞 || '名詞'}\t${word.説明 || ''}`;
    }).join('\n');

    downloadFile(txtContent, 'dictionary.txt', 'text/plain');
    showNotification(`📄 TXT形式で出力しました (${selectedCategories.length}カテゴリ, ${data.length}件)`, 'success');
}

function exportToMacOS() {
    const selectedCategories = getSelectedCategories();
    if (selectedCategories.length === 0) {
        showNotification('⚠️ エクスポートするカテゴリを選択してください', 'error');
        return;
    }

    const data = getCurrentCategoryData(selectedCategories);
    if (!data.length) {
        showNotification('⚠️ エクスポートするデータがありません', 'error');
        return;
    }

    // macOS用 .plist形式（Property List）
    const plistHeader = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<array>`;

    const plistFooter = `</array>
</plist>`;

    // 各単語をplist辞書エントリに変換
    const entries = data.map(word => {
        // XMLエスケープ
        const escapeXML = (str) => {
            if (!str) return '';
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&apos;');
        };

        return `	<dict>
		<key>phrase</key>
		<string>${escapeXML(word.単語)}</string>
		<key>shortcut</key>
		<string>${escapeXML(word.読み)}</string>
	</dict>`;
    }).join('\n');

    const plistContent = plistHeader + '\n' + entries + '\n' + plistFooter;

    downloadFile(plistContent, 'dictionary.plist', 'application/x-plist');
    showNotification(`🍎 macOS用plist形式で出力しました (${selectedCategories.length}カテゴリ, ${data.length}件)`, 'success');
}

function exportToWindows() {
    const selectedCategories = getSelectedCategories();
    if (selectedCategories.length === 0) {
        showNotification('⚠️ エクスポートするカテゴリを選択してください', 'error');
        return;
    }

    const data = getCurrentCategoryData(selectedCategories);
    if (!data.length) {
        showNotification('⚠️ エクスポートするデータがありません', 'error');
        return;
    }

    const windowsContent = [
        '!Microsoft IME Dictionary Tool',
        '!Version=10.0',
        '!CharSet=UTF-16LE',
        '!Format=<Reading>\t<Word>\t<POS>\t<Comment>',
        `!Categories: ${selectedCategories.join(', ')}`,
        '',
        ...data.map(word => `${word.読み}\t${word.単語}\t${word.品詞 || '名詞'}\t${word.説明 || ''}`)
    ].join('\n');

    downloadFile(windowsContent, 'dictionary_windows.txt', 'text/plain');
    showNotification(`🪟 Windows形式で出力しました (${selectedCategories.length}カテゴリ, ${data.length}件)`, 'success');
}

function getCurrentCategoryData(selectedCategories = null) {
    // 選択されたカテゴリが指定されている場合
    if (selectedCategories && selectedCategories.length > 0) {
        const words = [];
        selectedCategories.forEach(categoryKey => {
            const category = dictionaryData.カテゴリ[categoryKey];
            if (category && category.有効 !== false && category.単語リスト) {
                // カテゴリ名を各単語に追加
                category.単語リスト.forEach(word => {
                    words.push({ ...word, カテゴリ: categoryKey });
                });
            }
        });
        return words;
    }

    // 現在のカテゴリが選択されている場合
    if (currentCategory && dictionaryData.カテゴリ[currentCategory]) {
        return dictionaryData.カテゴリ[currentCategory].単語リスト || [];
    }

    // 全カテゴリの場合
    const allWords = [];
    Object.entries(dictionaryData.カテゴリ).forEach(([categoryKey, category]) => {
        if (category.有効 !== false && category.単語リスト) {
            category.単語リスト.forEach(word => {
                allWords.push({ ...word, カテゴリ: categoryKey });
            });
        }
    });
    return allWords;
}

function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], {type: mimeType + ';charset=utf-8;'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
}

// モーダル外クリックで閉じる
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
});

// 初期化
document.addEventListener('DOMContentLoaded', function() {
    updateUI();
    showNotification('📚 IME辞書管理ツールを開始しました', 'success');
});