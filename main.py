# main.py
from components.update_firestore import shift_updates, update_latest_articles

def main():
    try:
        print("シフト処理を開始します...")
        shift_updates()
        print("最新記事を Gemini API から取得中...")
        update_latest_articles()
        print("更新が完了しました。")
    except Exception as e:
        print("エラーが発生しました:", e)

if __name__ == "__main__":
    main()
