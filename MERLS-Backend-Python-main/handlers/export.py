from flask import Blueprint, request, send_file, jsonify
from SupabaseClient import supabase
import pandas as pd
import io

export_bp = Blueprint("export_bp", __name__)

@export_bp.route("/export", methods=["GET"])
def export_results():
    participant_id = request.args.get("participant_id")
    if not participant_id:
        return jsonify({"error": "Missing participant_id"}), 400

    language = request.args.get("language", "en")  # 默认值为 "en"
    is_en = language.lower() == "en"

    response = supabase.table("submissions").select("*") \
        .eq("participant_id", participant_id) \
        .eq("is_en", is_en).execute()

    # 安全检查
    if not response or "data" not in response or response["data"] is None:
        return jsonify({"error": "No data returned from Supabase"}), 500

    # 转换为 DataFrame
    df = pd.DataFrame(response["data"])
    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)

    return send_file(
        excel_file,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=f"{participant_id}_export.xlsx"
    )
