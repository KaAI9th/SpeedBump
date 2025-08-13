import random
import os
import sys
import turtle
# --- ▼ [신규] 도로 설계 파라미터 정의 ---
# 이 값들은 사용자의 .vroad 파일 구조를 기반으로 합니다.
# 종단곡선의 전체 길이 (BVC to EVC)
VCL = 3.6
# 종단곡선 시작점(BVC)에서 종단변화점(PVI)까지의 수평 거리
DISTANCE_TO_PVI = 1.3

# 파일 경로 설정
BASE_DIR = r'C:\Users\user\Desktop\이주혁의 배치시도'
Real_DIR = r'C:\Users\user\Desktop\이주혁의 배치시도\use_this'
INPUT_FILE = os.path.join(BASE_DIR, 'jh.vroad')
OUTPUT_FILE = os.path.join(Real_DIR, '수정된_jh.vroad')

# 도로의 기준 높이 (과속방지턱 시작점/종료점의 y좌표)
BASE_Y_VALUE = 596.5


# --- ▼ [수정] 정확한 공식에 기반한 계산 함수 ---
def calculate_pvi_y_from_actual_height(target_height):
    """
    목표 실제 높이(H)를 만들기 위해 필요한 PVI의 y좌표를 계산합니다.
    - 공식: 실제 높이 H = (g1 * L) / 4
    - 위 공식을 g1에 대해 정리: g1 = (4 * H) / L
    - g1과 PVI의 관계: g1 = (PVI_y - 기준_y) / PVI까지의_거리
    - 최종적으로 PVI_y에 대해 정리하여 값을 구합니다.
    """
    if VCL == 0: return BASE_Y_VALUE
    # 1. 목표 높이를 만들기 위한 진입 경사(g1) 계산
    g1 = (4 * target_height) / VCL
    # 2. 해당 g1을 만들기 위한 PVI의 y좌표 계산
    pvi_y = (g1 * DISTANCE_TO_PVI) + BASE_Y_VALUE
    return pvi_y

def calculate_actual_height_from_pvi_y(pvi_y):
    """
    PVI의 y좌표를 바탕으로 실제 과속방지턱의 높이를 역산합니다.
    """
    if DISTANCE_TO_PVI == 0: return 0.0
    # 1. PVI y좌표로부터 진입 경사(g1) 역산
    g1 = (pvi_y - BASE_Y_VALUE) / DISTANCE_TO_PVI
    # 2. g1을 이용해 실제 높이 계산
    actual_height = (g1 * VCL) / 4
    return actual_height

def main():
    if len(sys.argv) != 2:
        print("사용법: python vroad_modifier.py [1|2|3]")
        print("  1: 5cm ~ 10cm 실제 높이의 과속방지턱 생성")
        print("  2: 10cm ~ 25cm 실제 높이의 과속방지턱 생성")
        print("  3: 0cm 과속방지턱 생성")
        return

    mode = sys.argv[1]

    # 수정 대상이 될 과속방지턱 '정점(PVI)'의 원래 y값들
    target_y_values = {
        '597.5', '597.6', '597.7', '597.8', '597.9', '598',
        '598.1', '598.2', '598.3', '598.4', '598.5', '598.6'
    }

    # 목표 '실제 높이'를 기준으로 PVI y값 범위를 설정
    if mode == "1":
        min_height, max_height = 0.05, 0.10 # 목표 높이: 5cm ~ 10cm
        min_pvi_y = calculate_pvi_y_from_actual_height(min_height)
        max_pvi_y = calculate_pvi_y_from_actual_height(max_height)
        print(f"🎲 모드 1: {min_height*100:.0f}cm ~ {max_height*100:.0f}cm 실제 높이의 과속방지턱 생성")
    elif mode == "2":
        min_height, max_height = 0.10, 0.25 # 목표 높이: 10cm ~ 25cm
        min_pvi_y = calculate_pvi_y_from_actual_height(min_height)
        max_pvi_y = calculate_pvi_y_from_actual_height(max_height)
        print(f"🎲 모드 2: {min_height*100:.0f}cm ~ {max_height*100:.0f}cm 실제 높이의 과속방지턱 생성")
    elif mode == "3":
        min_height, max_height = 0.0, 0.0 # 목표 높이: 0cm
        min_pvi_y = calculate_pvi_y_from_actual_height(min_height)
        max_pvi_y = calculate_pvi_y_from_actual_height(max_height)
        print("📌 모드 3: 0cm 과속방지턱 생성")
    else:
        print("❌ 잘못된 모드입니다. 1, 2, 3 중 하나를 선택하세요.")
        return

    if not os.path.exists(INPUT_FILE):
        print(f"❌ 오류: 입력 파일을 찾을 수 없습니다!")
        print(f"파일 경로: {INPUT_FILE}")
        return

    os.makedirs(Real_DIR, exist_ok=True)

    try:
        with open(INPUT_FILE, 'rb') as infile:
            content_bytes = infile.read()
        content_str = content_bytes.decode('latin1')
        lines = content_str.splitlines(True)

        modified_lines = []
        modified_count = 0
        print("\n🔧 과속방지턱 PVI y좌표 수정 및 실제 높이 계산 중...")
        print("-" * 70)

        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith('point.y ='):
                try:
                    current_y_str = stripped_line.split('=')[1].strip()
                    if current_y_str in target_y_values:
                        
                        # 1. 목표 PVI y좌표 범위 내에서 랜덤 값 생성
                        new_pvi_y = round(random.uniform(min_pvi_y, max_pvi_y), 4) if min_pvi_y != max_pvi_y else min_pvi_y
                        
                        # 2. 생성된 PVI y좌표를 기반으로 '실제 높이'를 역산
                        actual_height = calculate_actual_height_from_pvi_y(new_pvi_y)
                        
                        # 3. 프롬프트에 표시할 값 (실제 높이 * 0.9)
                        prompt_display_height = actual_height * 0.9

                        # 4. 파일에 쓸 새로운 라인 생성 (PVI y좌표 수정)
                        indentation = line[:line.find('point.y')]
                        original_ending = line[len(line.rstrip('\r\n')):]
                        new_line = f"{indentation}point.y = {new_pvi_y}{original_ending}"
                        modified_lines.append(new_line)
                        
                        # --- ▼ [수정] 더 명확해진 출력문 ---
                        print(f"  [수정] PVI y: {new_pvi_y:<10.4f} -> 실제 높이: {actual_height*100:<5.2f}cm (프롬프트용: {prompt_display_height:.4f}m)")
                        
                        modified_count += 1
                        continue
                except (ValueError, IndexError):
                    pass
            modified_lines.append(line)

        updated_content_str = "".join(modified_lines)
        updated_content_bytes = updated_content_str.encode('latin1')

        with open(OUTPUT_FILE, 'wb') as outfile:
            outfile.write(updated_content_bytes)

        print("-" * 70)
        print(f"\n✅ {modified_count}개의 과속방지턱 높이가 성공적으로 수정되었습니다.")
        print(f"💾 파일이 '{OUTPUT_FILE}'로 저장되었습니다.")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()