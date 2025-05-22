# services/exercise_recommendation.py
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import NearestNeighbors
from collections import Counter

# ── 여기가 핵심 수정 부분 ──
# 현재 파일이 있는 디렉터리 (services)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# 프로젝트 루트 (…/MDN)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
# data 폴더 까지만 한 번만 붙이기
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

# 디버깅: 올바른 DATA_DIR 경로인지 꼭 한 번 찍어보세요!
print(f"[DEBUG] DATA_DIR = {DATA_DIR}")

# ── 그다음부터는 DATA_DIR만 사용 ──
df_gym      = pd.read_excel(os.path.join(DATA_DIR, 'gym_recommendation.xlsx'))
df_meta     = pd.read_csv(os.path.join(DATA_DIR, 'megaGymDataset.csv'), encoding='utf-8')
df_location = pd.read_csv(os.path.join(DATA_DIR, 'exercise_location_labels.csv'), encoding='utf-8')

equipment_map = {
    row['Title'].strip().lower(): 
      set(e.strip().lower() for e in str(row['Equipment']).split(',') if e.strip())
    for _, row in df_meta.iterrows()
}

# 레이블 인코더 준비
label_cols = ['Sex','Hypertension','Diabetes','Fitness Goal','Fitness Type','Level']
encoders   = {col: LabelEncoder().fit(df_gym[col]) for col in label_cols}
for col, le in encoders.items():
    df_gym[col] = le.transform(df_gym[col])

feature_cols = ['Sex','Age','Height','Weight','Hypertension','Diabetes','BMI','Level','Fitness Goal','Fitness Type']
scaler = StandardScaler().fit(df_gym[feature_cols])
X_scaled = scaler.transform(df_gym[feature_cols])
knn = NearestNeighbors(n_neighbors=5, metric='euclidean').fit(X_scaled)

def is_home_friendly(ex_name: str) -> bool:
    row = df_location[df_location['Exercise'].str.lower() == ex_name.lower()]
    if row.empty: return True
    return 'home' in row.iloc[0]['Location'].lower()

def get_exercise_recommendation(user_input: dict) -> list[str]:
    """
    user_input 예시 키:
      Sex, Age, Height, Weight,
      Hypertension, Diabetes, BMI,
      Level, Fitness Goal, Fitness Type,
      Workout Environment
    """
    new_df = pd.DataFrame([user_input])
    # 레이블 인코딩
    for col, le in encoders.items():
        val = new_df.at[0, col]
        new_df.at[0, col] = le.transform([val])[0] if val in le.classes_ else -1
    X_new = scaler.transform(new_df[feature_cols])

    # KNN 이웃 탐색
    _, idxs = knn.kneighbors(X_new)

    user_equip = user_input.get('Equipment', 'none')  # ex: 'none', 'dumbbells', 'bands' 등
    env        = user_input.get('Workout Environment', 'home').lower()

    ex_list = []
    for i in idxs[0]:
        raw = str(df_gym.at[i, 'Exercises']).replace(' and ', ',')
        for ex in raw.split(','):
            ex = ex.strip()
            key = ex.lower()

            # ① 환경 필터
            if env == 'home' and not is_home_friendly(ex):
                continue

            # ② 기구 필터
            required = equipment_map.get(key, set())
            # 사용자가 장비 없음 → 필요한 기구가 있으면 스킵
            if user_equip == 'none' and required:
                continue
            # 사용자가 특정 기구 보유 → 그 기구 없으면 스킵
            if user_equip != 'none' and required and user_equip not in required:
                continue

            if ex:
                ex_list.append(ex)

    # Top5 빈도순 반환
    return [ex for ex, _ in Counter(ex_list).most_common(5)]
    
