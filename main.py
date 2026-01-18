import cv2
from collections import defaultdict
from ultralytics import YOLO

# COCO: car=2, motorcycle=3, bus=5, truck=7
VEHICLE_CLASS_IDS = [2, 3, 5, 7]

VIDEO_PATH = "videos/rodovia.mp4"
MODEL_PATH = "models/yolov8n.pt"

CONF = 0.12
IMGSZ = 1280

# ZONA de contagem (faixa horizontal)
ZONE_CENTER_Y_RATIO = 0.48
ZONE_HALF_HEIGHT_PX = 55  # faixa total = 110px (aumente se ainda perder)

# Debounce (evita contar repetido na mesma posição)
COUNT_COOLDOWN_FRAMES = 25  # aumente se contar a mais / diminua se contar a menos

def center_xyxy(x1, y1, x2, y2):
    return int((x1 + x2) / 2), int((y1 + y2) / 2)

def in_zone(y, top, bottom):
    return top <= y <= bottom

def draw_panel(frame, total, per_class):
    overlay = frame.copy()

    x1, y1 = 20, 20
    x2, y2 = 430, 180

    cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

    cv2.putText(frame, f"TOTAL: {total}", (x1 + 20, y1 + 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 255), 3)

    cv2.putText(frame, f"CARROS: {per_class['car']}", (x1 + 20, y1 + 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.putText(frame, f"MOTOS: {per_class['motorcycle']}", (x1 + 20, y1 + 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.putText(frame, f"ONIBUS: {per_class['bus']}", (x1 + 20, y1 + 150),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.putText(frame, f"CAMINHAO: {per_class['truck']}", (x1 + 230, y1 + 150),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

def main():
    model = YOLO(MODEL_PATH)

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("❌ Não consegui abrir o vídeo.")
        return

    window_name = "SINVIA - Contagem por Zona (Entrada)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 960, 540)

    total = 0
    per_class = defaultdict(int)

    # Estado de entrada na zona por "chave do objeto"
    prev_in_zone = {}

    # Último frame contado por chave (debounce)
    last_count_frame = {}

    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1

        h, w = frame.shape[:2]
        zone_center_y = int(h * ZONE_CENTER_Y_RATIO)
        zone_top = zone_center_y - ZONE_HALF_HEIGHT_PX
        zone_bottom = zone_center_y + ZONE_HALF_HEIGHT_PX

        # desenha zona
        cv2.rectangle(frame, (0, zone_top), (w, zone_bottom), (0, 255, 255), 2)

        results = model.track(
            frame,
            conf=CONF,
            imgsz=IMGSZ,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False
        )

        if results and results[0].boxes is not None:
            boxes = results[0].boxes

            for box in boxes:
                cls_id = int(box.cls[0])
                if cls_id not in VEHICLE_CLASS_IDS:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx, cy = center_xyxy(x1, y1, x2, y2)

                # ✅ ponto inferior da bbox (motos contam melhor assim)
                cy_bottom = y2

                name = model.names[cls_id]

                # desenha bbox + centro
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

                # ✅ CHAVE DO OBJETO:
                if box.id is not None:
                    track_id = int(box.id[0])
                    key = f"id_{track_id}"
                    label = f"ID {track_id} {name}"
                else:
                    key = f"pos_{cx//60}_{cy//60}_{cls_id}"
                    label = f"{name} (sem ID)"

                cv2.putText(frame, label, (x1, max(20, y1 - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                was_in_zone = prev_in_zone.get(key, False)

                # ✅ regra da zona: moto usa a base da bbox, outros usam o centro
                if cls_id == 3:  # motorcycle
                    now_in_zone = in_zone(cy_bottom, zone_top, zone_bottom)
                else:
                    now_in_zone = in_zone(cy, zone_top, zone_bottom)

                prev_in_zone[key] = now_in_zone

                # ✅ Evento: ENTROU na zona
                if (not was_in_zone) and now_in_zone:
                    last_f = last_count_frame.get(key, -9999)

                    if (frame_idx - last_f) > COUNT_COOLDOWN_FRAMES:
                        total += 1
                        per_class[name] += 1
                        last_count_frame[key] = frame_idx

        draw_panel(frame, total, per_class)

        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
