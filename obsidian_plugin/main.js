const { Plugin, Notice, Modal, TFolder } = require("obsidian");

// --- フォルダ名入力用モーダル ---
class FolderNameModal extends Modal {
  constructor(app, onSubmit) {
    super(app);
    this.onSubmit = onSubmit;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.createEl("h2", { text: "新しい周回のフォルダ名を入力" });

    const input = contentEl.createEl("input", {
      type: "text",
      placeholder: "例: 現場の問題",
    });

    input.focus();

    const submitBtn = contentEl.createEl("button", { text: "開始" });
    submitBtn.onclick = () => {
      const value = input.value.trim();
      if (value) {
        this.onSubmit(value);
        this.close();
      }
    };
  }

  onClose() {
    this.contentEl.empty();
  }
}

module.exports = class MyMinimalPlugin extends Plugin {
  async onload() {
    console.log("My Minimal Plugin loaded");

    this.currentSessionId = null;
    this.currentFolderName = null;

    // --- Hello コマンド ---
    this.addCommand({
      id: "hello-thinkring",
      name: "Hello from thinkRing",
      callback: () => {
        new Notice("thinkRing plugin is working!");
      }
    });

    // --- thinkRing: 新しいノードを作成 ---
    this.addCommand({
      id: "thinkring-create-node",
      name: "thinkRing: 新しいノードを作成",
      callback: async () => {
        const timestamp = window.moment().format("YYYY-MM-DD_HHmmss");
        const session = this.currentSessionId ?? "none";

        let basePath = "";
        if (this.currentFolderName) {
          basePath = `thinkRing/${this.currentFolderName}/`;
        }

        const fileName = `${timestamp}_Node.md`;

        const template = `---
keywords: []
created: ${timestamp}
type: node
session: ${session}
---

# thinkRing Node
context:

`;

        const file = await this.app.vault.create(basePath + fileName, template);
        await this.app.workspace.getLeaf().openFile(file);

        new Notice("thinkRing ノードを作成しました");
      }
    });

    // --- thinkRing: 新しい1周目を開始 ---
    this.addCommand({
      id: "thinkring-start-first-round",
      name: "thinkRing: 新しい1周目を開始",
      callback: async () => {
        new FolderNameModal(this.app, async (folderNameInput) => {
          // 毎回新しいセッションIDを発行
          const sessionId = window.moment().format("YYYY-MM-DD_HHmmss");
          this.currentSessionId = sessionId;

          // ベースフォルダ thinkRing を保証
          const baseFolder = "thinkRing";
          if (!this.app.vault.getAbstractFileByPath(baseFolder + "/")) {
            await this.app.vault.createFolder(baseFolder);
          }

          const folderName = `thinkRing-${folderNameInput}`;
          const folderPath = `${baseFolder}/${folderName}/`;

          this.currentFolderName = folderName;

          if (!this.app.vault.getAbstractFileByPath(folderPath)) {
            await this.app.vault.createFolder(folderPath);
          }

          const steps = [
            {
              title: "Step1-問題の明確化",
              step: 1,
              body: `## Step1 - 問題の明確化
問題を一言で書く:

`
            },
            {
              title: "Step2-要因の洗い出し",
              step: 2,
              body: `## Step2 - 要因の洗い出し

### 要因リスト
1.
2.
3.
4.
5.

`
            },
            {
              title: "Step3-仮説の生成",
              step: 3,
              body: `## Step3 - 仮説の生成

### 仮説の型（参考）
- もし A なら B になる
- A が起きているのは B が原因である
- A を改善するには B を変える必要がある
- A の背景には B という構造がある

### 仮説リスト（※仮説は3つまで）
1.
2.
3.

### 根拠
- 
- 
- 

### 反証ポイント（検証の視点）
- 
- 
- 

### 関連ノート
- [[Step1-問題の明確化]]
- [[Step2-要因の洗い出し]]

`
            },
            {
              title: "Step4-検証の方向性",
              step: 4,
              body: `## Step4 - 検証の方向性
どう検証するか:

`
            },
            {
              title: "Step5-次のアクション",
              step: 5,
              body: `## Step5 - 次のアクション
次に何をするか:

`
            }
          ];

          const createdFiles = [];

          for (let i = 0; i < steps.length; i++) {
            const timestamp = window.moment().format("YYYY-MM-DD_HHmmss");
            const fileName = `${timestamp}_${steps[i].title}.md`;

            const frontmatter = `---
keywords: []
step: ${steps[i].step}
type: round
session: ${sessionId}
folder: ${folderNameInput}
---`;

            const fileContent = `${frontmatter}

${steps[i].body}`;

            const file = await this.app.vault.create(folderPath + fileName, fileContent);
            createdFiles.push(file);
          }

          // --- 前後リンク ---
          for (let i = 0; i < createdFiles.length; i++) {
            let content = await this.app.vault.read(createdFiles[i]);

            const prev = createdFiles[i - 1];
            const next = createdFiles[i + 1];

            if (prev) {
              const prevLink = `[[thinkRing/${this.currentFolderName}/${prev.name}|← 前へ]]`;
              content += `\n${prevLink}`;
            }

            if (next) {
              const nextLink = `[[thinkRing/${this.currentFolderName}/${next.name}|次へ →]]`;
              content += `\n${nextLink}`;
            }

            await this.app.vault.modify(createdFiles[i], content);
          }

          await this.app.workspace.getLeaf().openFile(createdFiles[0]);

          new Notice(`thinkRing 1周目を開始しました（フォルダ: thinkRing/${folderName}）`);
        }).open();
      }
    });

    // --- phase4: 周回一覧ビュー（Vault 全体から検出 / Sessions は thinkRing 内） ---
    this.addCommand({
      id: "thinkring-session-list",
      name: "thinkRing: 周回一覧を開く",
      callback: async () => {
        // ベースフォルダ thinkRing を保証
        const baseFolderPath = "thinkRing/";
        let baseFolder = this.app.vault.getAbstractFileByPath(baseFolderPath);
        if (!baseFolder) {
          baseFolder = await this.app.vault.createFolder("thinkRing");
        }

        if (!(baseFolder instanceof TFolder)) {
          new Notice("thinkRing フォルダが正しく認識できませんでした。");
          return;
        }

        // --- Vault 全体を再帰的に探索して thinkRing- フォルダを検出 ---
        const folders = [];
        const root = this.app.vault.getRoot();

        const recurse = (folder) => {
          for (const child of folder.children) {
            if (child instanceof TFolder) {
              if (child.name.startsWith("thinkRing-")) {
                folders.push(child);
              }
              recurse(child);
            }
          }
        };

        recurse(root);

        let listContent = `# thinkRing 周回一覧\n\n## 過去の周回\n`;

        if (folders.length === 0) {
          listContent += `まだ周回がありません。\n「thinkRing: 新しい1周目を開始」から始めてください。\n`;
        } else {
          for (const folder of folders) {
            const step1 = folder.children.find(f => f.name.includes("Step1-問題の明確化"));
            if (step1) {
              const text = await this.app.vault.read(step1);
              const sessionMatch = text.match(/session:\s*(.*)/);
              const sessionId = sessionMatch ? sessionMatch[1].trim() : "unknown";

              // フォルダのパスをそのままリンクに使う（どこにあっても対応）
              const linkPath = folder.path; // 例: "thinkRing/thinkRing-現場の問題" or "thinkRing-現場の問題"
              listContent += `- [[${linkPath}|${folder.name}]]（session: ${sessionId}）\n`;
            }
          }
        }

        const listFilePath = "thinkRing/thinkRing-Sessions.md";
        const existing = this.app.vault.getAbstractFileByPath(listFilePath);

        if (existing) {
          await this.app.vault.modify(existing, listContent);
        } else {
          await this.app.vault.create(listFilePath, listContent);
        }

        const file = this.app.vault.getAbstractFileByPath(listFilePath);
        await this.app.workspace.getLeaf().openFile(file);

        new Notice("thinkRing 周回一覧を更新しました");
      }
    });
  }

  onunload() {
    console.log("My Minimal Plugin unloaded");
  }
};