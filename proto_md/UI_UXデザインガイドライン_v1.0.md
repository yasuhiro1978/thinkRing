# UI/UXデザインガイドライン（Design Guidelines）
## プロジェクト名：thinkRing
## バージョン：v1.0
## 作成者：yasuhiro

---

# 1. 概要（Overview）

本ガイドラインは、thinkRingアプリケーションのUI/UXデザインの統一性と一貫性を保つための基準を定義する。  
ユーザーが思考プロセスを効率的に構造化できるよう、シンプルで直感的なインターフェースを目指す。

---

# 2. デザイン原則（Design Principles）

## 2.1 シンプルさ（Simplicity）

- 不要な装飾を排除
- 情報の階層を明確に
- 1画面1機能を原則

## 2.2 一貫性（Consistency）

- 同じ機能は同じUIパターンを使用
- ナビゲーション構造を統一
- 用語とアイコンの統一

## 2.3 効率性（Efficiency）

- 操作ステップを最小化
- キーボードショートカットの提供
- 自動保存機能

## 2.4 アクセシビリティ（Accessibility）

- WCAG 2.1 AA準拠
- キーボード操作対応
- スクリーンリーダー対応

---

# 3. カラーパレット（Color Palette）

## 3.1 プライマリカラー

| 色 | カラーコード | 用途 |
|---|------------|------|
| Primary Blue | `#2563EB` | メインアクション、リンク |
| Primary Dark | `#1E40AF` | ホバー状態 |
| Primary Light | `#3B82F6` | アクティブ状態 |

## 3.2 セカンダリカラー

| 色 | カラーコード | 用途 |
|---|------------|------|
| Secondary Green | `#10B981` | 成功、完了状態 |
| Secondary Orange | `#F59E0B` | 警告、注意 |
| Secondary Red | `#EF4444` | エラー、削除 |

## 3.3 ニュートラルカラー

| 色 | カラーコード | 用途 |
|---|------------|------|
| Gray 900 | `#111827` | テキスト（主要） |
| Gray 700 | `#374151` | テキスト（セカンダリ） |
| Gray 500 | `#6B7280` | テキスト（補助） |
| Gray 300 | `#D1D5DB` | ボーダー |
| Gray 100 | `#F3F4F6` | 背景（セカンダリ） |
| White | `#FFFFFF` | 背景（プライマリ） |

## 3.4 セマンティックカラー

| 状態 | カラーコード | 用途 |
|-----|------------|------|
| Success | `#10B981` | 成功メッセージ |
| Warning | `#F59E0B` | 警告メッセージ |
| Error | `#EF4444` | エラーメッセージ |
| Info | `#3B82F6` | 情報メッセージ |

---

# 4. タイポグラフィ（Typography）

## 4.1 フォントファミリー

### 日本語
- **メインフォント**: "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Noto Sans JP", sans-serif
- **等幅フォント**: "SF Mono", "Monaco", "Consolas", monospace

### 英語
- **メインフォント**: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
- **等幅フォント**: "SF Mono", "Monaco", "Consolas", monospace

## 4.2 フォントサイズ

| 要素 | サイズ | 行間 | 用途 |
|-----|--------|------|------|
| H1 | 32px | 1.2 | ページタイトル |
| H2 | 24px | 1.3 | セクションタイトル |
| H3 | 20px | 1.4 | サブセクション |
| Body | 16px | 1.5 | 本文 |
| Small | 14px | 1.5 | 補助テキスト |
| Caption | 12px | 1.4 | キャプション |

## 4.3 フォントウェイト

- **Regular**: 400（本文）
- **Medium**: 500（強調）
- **Semibold**: 600（見出し）
- **Bold**: 700（重要）

---

# 5. スペーシング（Spacing）

## 5.1 スペーシングスケール

| サイズ | 値 | 用途 |
|-------|-----|------|
| xs | 4px | 最小間隔 |
| sm | 8px | 小間隔 |
| md | 16px | 標準間隔 |
| lg | 24px | 大間隔 |
| xl | 32px | 特大間隔 |
| 2xl | 48px | セクション間隔 |

## 5.2 レイアウトパディング

- **コンテナパディング**: 24px
- **カードパディング**: 16px
- **フォーム要素間隔**: 16px

---

# 6. コンポーネント（Components）

## 6.1 ボタン（Button）

### プライマリボタン

```css
.button-primary {
  background-color: #2563EB;
  color: #FFFFFF;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  border: none;
  cursor: pointer;
}

.button-primary:hover {
  background-color: #1E40AF;
}
```

### セカンダリボタン

```css
.button-secondary {
  background-color: transparent;
  color: #2563EB;
  padding: 12px 24px;
  border-radius: 8px;
  border: 1px solid #2563EB;
  cursor: pointer;
}
```

### ボタンサイズ

- **Small**: padding: 8px 16px, font-size: 14px
- **Medium**: padding: 12px 24px, font-size: 16px
- **Large**: padding: 16px 32px, font-size: 18px

## 6.2 入力フィールド（Input Field）

```css
.input-field {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #D1D5DB;
  border-radius: 8px;
  font-size: 16px;
}

.input-field:focus {
  outline: none;
  border-color: #2563EB;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}
```

## 6.3 カード（Card）

```css
.card {
  background-color: #FFFFFF;
  border: 1px solid #D1D5DB;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
```

## 6.4 モーダル（Modal）

```css
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background-color: #FFFFFF;
  border-radius: 12px;
  padding: 24px;
  max-width: 500px;
  width: 90%;
}
```

---

# 7. レイアウト（Layout）

## 7.1 グリッドシステム

- **コンテナ最大幅**: 1200px
- **グリッドカラム**: 12カラム
- **ガター**: 24px

## 7.2 レスポンシブブレークポイント

```css
/* モバイル */
@media (max-width: 768px) {
  .container {
    padding: 16px;
  }
}

/* タブレット */
@media (min-width: 769px) and (max-width: 1024px) {
  .container {
    padding: 24px;
  }
}

/* デスクトップ */
@media (min-width: 1025px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 32px;
  }
}
```

---

# 8. アイコン（Icons）

## 8.1 アイコンライブラリ

- **推奨**: Heroicons / Lucide Icons
- **サイズ**: 20px, 24px, 32px
- **色**: カラーパレットに準拠

## 8.2 主要アイコン

| 機能 | アイコン | サイズ |
|-----|---------|--------|
| プロジェクト作成 | Plus | 24px |
| 編集 | Pencil | 20px |
| 削除 | Trash | 20px |
| 保存 | Check | 24px |
| キャンセル | X | 20px |
| ナビゲーション | ChevronRight | 20px |

---

# 9. アニメーション（Animation）

## 9.1 トランジション

```css
/* 標準トランジション */
.transition {
  transition: all 0.2s ease-in-out;
}

/* ホバーエフェクト */
.hover-lift {
  transition: transform 0.2s ease-in-out;
}

.hover-lift:hover {
  transform: translateY(-2px);
}
```

## 9.2 アニメーション原則

- **持続時間**: 200ms〜300ms
- **イージング**: ease-in-out
- **過度なアニメーションは避ける**

---

# 10. フォームデザイン（Form Design）

## 10.1 フォーム要素

### ラベル

```css
.form-label {
  display: block;
  font-weight: 500;
  margin-bottom: 8px;
  color: #111827;
}
```

### エラーメッセージ

```css
.error-message {
  color: #EF4444;
  font-size: 14px;
  margin-top: 4px;
}
```

### 成功メッセージ

```css
.success-message {
  color: #10B981;
  font-size: 14px;
  margin-top: 4px;
}
```

## 10.2 バリデーション表示

- リアルタイムバリデーション
- エラー時は赤いボーダー
- 成功時は緑のチェックマーク

---

# 11. ナビゲーション（Navigation）

## 11.1 メインナビゲーション

- **位置**: 上部固定
- **高さ**: 64px
- **背景**: 白、影あり

## 11.2 パンくずリスト

- 現在位置を明確に表示
- クリックで上位階層に戻れる

## 11.3 サイドバー（将来）

- プロジェクト一覧
- ノード一覧
- 折りたたみ可能

---

# 12. フィードバック（Feedback）

## 12.1 ローディング状態

```css
.loading-spinner {
  border: 3px solid #F3F4F6;
  border-top: 3px solid #2563EB;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
}
```

## 12.2 トースト通知

- **成功**: 緑色、3秒表示
- **エラー**: 赤色、5秒表示
- **情報**: 青色、3秒表示

## 12.3 空状態

- アイコンとメッセージを表示
- アクションを促すボタン

---

# 13. アクセシビリティ（Accessibility）

## 13.1 キーボード操作

- Tab: フォーカス移動
- Enter: アクション実行
- Escape: モーダル閉じる
- Arrow keys: リスト内移動

## 13.2 ARIA属性

```html
<button aria-label="プロジェクトを削除">
  <TrashIcon />
</button>
```

## 13.3 コントラスト比

- 本文テキスト: 4.5:1以上
- 大きなテキスト: 3:1以上

---

# 14. ダークモード（将来）

## 14.1 カラーパレット（ダーク）

- **背景**: `#111827`
- **カード**: `#1F2937`
- **テキスト**: `#F9FAFB`

## 14.2 実装方針

- CSS変数を使用
- ユーザー設定で切り替え
- システム設定に追従

---

# 15. モバイル最適化

## 15.1 タッチ操作

- **タップ領域**: 最小44x44px
- **スワイプ**: リスト操作
- **長押し**: コンテキストメニュー

## 15.2 モバイル特有のUI

- ボトムシート（モーダル代替）
- プルリフレッシュ
- 無限スクロール

---

# 16. パフォーマンス

## 16.1 画像最適化

- WebP形式を使用
- 遅延読み込み
- 適切なサイズ

## 16.2 レンダリング最適化

- 仮想スクロール（大量リスト）
- コード分割
- レイジーローディング

---

# 17. ブランディング

## 17.1 ロゴ

- **配置**: 左上
- **サイズ**: 32px高さ
- **クリック**: ホームに戻る

## 17.2 ファビコン

- 16x16, 32x32, 48x48, 192x192, 512x512
- 全サイズを用意

---

# 18. 実装ガイドライン

## 18.1 CSS設計

- **方法論**: BEM（Block Element Modifier）
- **命名規則**: ケバブケース

```css
.card { }
.card__title { }
.card--featured { }
```

## 18.2 コンポーネント設計

- 再利用可能なコンポーネント
- Propsでカスタマイズ
- デフォルト値の設定

---

# 19. デザインシステムツール

## 19.1 推奨ツール

- **デザイン**: Figma
- **コンポーネント**: Storybook（将来）
- **ドキュメント**: 本ガイドライン

## 19.2 デザインファイル

- コンポーネントライブラリ
- デザイントークン
- プロトタイプ

---

# 20. 備考

- 本ガイドラインは MVP 版を前提とする
- ユーザーフィードバックに基づいて改善
- 定期的に見直しを行う

