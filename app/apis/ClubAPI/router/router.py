from fastapi import APIRouter, File, Query, UploadFile, Request
from typing import Optional
from fastapi.responses import FileResponse
from app.apis.ClubAPI.service.club_service import delete_club_file, download_club_file, find_clubs, create_new_club, get_club_members, get_tags_by_catagory, update_club_information, get_club_brief, upload_clubdetail_file
from app.apis.ClubAPI.Models.clubmodel import ClubDetail, ClubDetailEdit
from app.common.response.formatter import error_response, success_response

router = APIRouter()

@router.get("/club/tags")
async def get_tag_list():
    try:
        # 태그 목록을 서비스에서 가져옵니다.
        tags = get_tags_by_catagory()
        # 성공 응답으로 태그 목록 반환
        return success_response(data=tags, message="태그 목록이 성공적으로 조회되었습니다.")
    except Exception as e:
        return error_response(error="SERVER_ERROR", message=str(e))

@router.get("/club/members")
async def club_members(request: Request, club_id: int = Query(...)):
    if not club_id:
        return error_response(error="INVALID_INPUT", message="club_id는 필수 입력입니다.")
    try:
        logined_user_info = getattr(request.state, "member_info", None)
        if not logined_user_info:
            return error_response(error="UNAUTHORIZED", message="로그인된 사용자 정보를 찾을 수 없습니다.")
        
        logined_user_id = logined_user_info.get("sub")
        if not logined_user_id:
            return error_response(error="UNAUTHORIZED", message="사용자 ID를 확인할 수 없습니다.")
        
        members = get_club_members(logined_user_id, club_id)
        return success_response(data={"member_ids": members}, message="Club members retrieved successfully")
      
    except Exception as e:
        return error_response(error="SERVER_ERROR", message=str(e))
    except PermissionError as e:
        return error_response(error="FORBIDDEN", message=str(e))

@router.get("/club/brief")
async def club_brief(club_id: int):
    try:
        result = get_club_brief(club_id)
        return success_response(data=result, message="Club brief retrieved successfully.")
        
    except ValueError as e:
        return error_response(error="NOT_FOUND", message=str(e))

@router.patch("/club/detailedit")
async def update_club_detail(login_request: Request, request: ClubDetailEdit):
    try:
        logined_user_info = getattr(login_request.state, "member_info", None)
        if not logined_user_info:
            return error_response(error="UNAUTHORIZED", message="로그인된 사용자 정보를 찾을 수 없습니다.")
        
        logined_user_id = logined_user_info.get("sub")
        if not logined_user_id:
            return error_response(error="UNAUTHORIZED", message="사용자 ID를 확인할 수 없습니다.")
        update_club_information(
            request.club_id,
            request.description,
            request.study_count,
            request.award_count,
            request.edu_count,
            request.event_count,
            request.established_date,
            request.location,
            logined_user_id
        )
        return success_response(data=None, message="동아리 정보가 성공적으로 수정되었습니다.")
    
    except ValueError as e:
        return error_response(error="INVALID_INPUT", message=str(e))
    except PermissionError as e:
        return error_response(error="FORBIDDEN", message=str(e))

@router.patch("/club/detailedit/files") #file upload
async def upload_file(request: Request, club_id: int, file: UploadFile = File(...)):
    try:
        logined_user_info = getattr(request.state, "member_info", None)
        if not logined_user_info:
            return error_response(error="UNAUTHORIZED", message="로그인된 사용자 정보를 찾을 수 없습니다.")
        
        logined_user_id = logined_user_info.get("sub")
        if not logined_user_id:
            return error_response(error="UNAUTHORIZED", message="사용자 ID를 확인할 수 없습니다.")
        
        # 서비스 계층으로 파일 업로드 요청 전달
        result = await upload_clubdetail_file(file, logined_user_id, club_id)
        return success_response(data=result, message="파일이 성공적으로 업로드되었습니다.")
    
    except Exception as e:
        return error_response(error="SERVER_ERROR", message=str(e))
    except PermissionError as e:
        return error_response(error="FORBIDDEN", message=str(e))

@router.get("/club/detailedit/{file_id}") #file download
async def download_file(request: Request, file_id: int):
    try:
        logined_user_info = getattr(request.state, "member_info", None)
        if not logined_user_info:
            return error_response(error="UNAUTHORIZED", message="로그인된 사용자 정보를 찾을 수 없습니다.")
        
        logined_user_id = logined_user_info.get("sub")
        if not logined_user_id:
            return error_response(error="UNAUTHORIZED", message="사용자 ID를 확인할 수 없습니다.")

        file_path, original_filename = download_club_file(file_id, logined_user_id)
        return FileResponse(file_path, media_type="application/octet-stream", filename=original_filename)
    except ValueError as e:
        return error_response(error="NOT_FOUND", message=str(e))
    except Exception as e:
        return error_response(error="SERVER_ERROR", message=str(e))

@router.delete("/club/detailedit/{file_id}") #file delete
async def delete_file(request: Request, file_id: int):
    try:
        logined_user_info = getattr(request.state, "member_info", None)
        if not logined_user_info:
            return error_response(error="UNAUTHORIZED", message="로그인된 사용자 정보를 찾을 수 없습니다.")
        
        logined_user_id = logined_user_info.get("sub")
        if not logined_user_id:
            return error_response(error="UNAUTHORIZED", message="사용자 ID를 확인할 수 없습니다.")
        
        delete_club_file(file_id, logined_user_id)
        return success_response(message="파일이 성공적으로 삭제되었습니다.")
    except ValueError as e:
        return error_response(error="INVALID_INPUT", message=str(e))
    except Exception as e:
        return error_response(error="SERVER_ERROR", message=str(e))

@router.post("/club/create")
async def create_club(request: ClubDetail):  # 동아리 추가
    try:
        result = create_new_club(
            name=request.name,
            club_depart=request.club_depart,
            club_type=request.club_type,
            president_id=request.president_id
        )
        if result:
            return success_response(data=result, message="Club created successfully")
        else:
            return error_response(error="INVALID_INPUT", message=result.get("message"))
    except Exception as e:
        return error_response(error="SERVER_ERROR", message=str(e))

@router.get("/club/find")
def get_club(
    club_name: Optional[str] = None, 
    tag_ids: Optional[list[int]] = Query([], alias="tag_id")  # 여러 개의 태그 ID
):  
    try:
        result = find_clubs(name=club_name, tag_ids=tag_ids)
        if 'success' not in result or not result['success']:
            return error_response(error="NOT_FOUND", message=result.get("message", "No message available"))

        return success_response(data=result.get("data"), message=result.get("message"))
    
    except Exception as e:
        return error_response(error="SERVER_ERROR", message=str(e))
    except ValueError as ve:
        return error_response(error="VALUES_ERROR", message=str(ve))