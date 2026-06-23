from abc import ABC, abstractmethod

# ==============================================================================
# CLASS CƠ SỞ TRƯỜNG TƯỢNG (ABSTRACT BASE CLASS)
# ==============================================================================
class BaseLesson(ABC):
    """
    Lớp trừu tượng định nghĩa bộ khung chuẩn cho mọi bài học trên hệ thống LMS.
    Sử dụng decorator @abstractmethod để bắt buộc các lớp con phải ghi đè.
    """
    # Class Attributes (Thuộc tính cấp lớp áp dụng toàn hệ thống)
    platform_name = "Rikkei Academy LMS"
    base_completion_points = 10

    def __init__(self, lesson_code: str, title: str):
        # Kiểm tra tính hợp lệ của mã bài học ngay khi khởi tạo thông qua Static Method
        if not self.validate_lesson_code(lesson_code):
            raise ValueError("Mã bài học không hợp lệ! Phải gồm đúng 10 ký tự và bắt đầu bằng LMS.")
        
        self._lesson_code = lesson_code
        self._title = ""
        self.title = title  # Gọi setter để tự động chuẩn hóa tiêu đề bài học
        
        # Private Attribute: Đóng gói nghiêm ngặt thời lượng bài học (phút)
        self.__duration_minutes = 0.0

    # --------------------------------------------------------------------------
    # GETTER / SETTER PROPERTIES
    # --------------------------------------------------------------------------
    @property
    def lesson_code(self) -> str:
        return self._lesson_code

    @property
    def title(self) -> str:
        return self._title

    @name_setter := title.setter
    def title(self, value: str):
        """Tự động chuẩn hóa tiêu đề bài học: In hoa và loại bỏ khoảng trắng thừa"""
        if value:
            self._title = " ".join(value.strip().split()).upper()
        else:
            self._title = ""

    @property
    def duration_minutes(self) -> float:
        """
        Property chỉ có Getter để đọc thời lượng hiện tại.
        Tuyệt đối không có Setter trực tiếp nhằm chặn hành vi tự ý thay đổi thời lượng bài học từ bên ngoài.
        """
        return self.__duration_minutes

    # Phương thức nội bộ hỗ trợ thiết lập/cập nhật thời lượng an toàn từ bên trong hệ thống
    def _set_duration_minutes(self, minutes: float):
        if minutes <= 0:
            raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0.")
        self.__duration_minutes = minutes

    # --------------------------------------------------------------------------
    # ABSTRACT METHODS (CÁC PHƯƠNG THỨC TRƯỜNG TƯỢNG)
    # --------------------------------------------------------------------------
    @abstractmethod
    def calculate_completion_score(self) -> float:
        """Tính toán điểm kinh nghiệm (XP) hoàn thành bài học (Bắt buộc ghi đè)"""
        pass

    @abstractmethod
    def update_content(self, new_data):
        """Cập nhật các thông số nội dung đặc thù của từng loại bài học (Bắt buộc ghi đè)"""
        pass

    # --------------------------------------------------------------------------
    # OPERATOR OVERLOADING (NẠP CHỒNG TOÁN TỬ)
    # --------------------------------------------------------------------------
    def __add__(self, other):
        """
        Nạp chồng toán tử cộng (+): Gộp thời lượng của hai bài học.
        Bẫy dữ liệu: Kiểm tra tính tương thích loại đối tượng (Edge Case 3).
        """
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes + other.duration_minutes

    def __lt__(self, other) -> bool:
        """
        Nạp chồng toán tử so sánh nhỏ hơn (<): So sánh thời lượng bài học.
        Bẫy dữ liệu: Kiểm tra tính tương thích loại đối tượng (Edge Case 3).
        """
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes < other.duration_minutes

    # --------------------------------------------------------------------------
    # STATIC & CLASS METHODS
    # --------------------------------------------------------------------------
    @staticmethod
    def validate_lesson_code(lesson_code: str) -> bool:
        """
        @staticmethod: Hàm tiện ích độc lập kiểm tra định dạng mã bài học đầu vào.
        Yêu cầu bắt đầu bằng cụm từ cố định 'LMS' và độ dài đúng 10 ký tự.
        """
        return isinstance(lesson_code, str) and len(lesson_code) == 10 and lesson_code.startswith("LMS")

    @classmethod
    def update_base_points(cls, new_points: int):
        """
        @classmethod: Nhận đối số đầu tiên là lớp (cls) để cập nhật đồng bộ
        điểm hoàn thành cơ bản áp dụng cho toàn bộ bài học trên hệ thống.
        """
        if new_points < 0:
            raise ValueError("Điểm cơ sở không được là số âm.")
        cls.base_completion_points = new_points


# ==============================================================================
# SUBCLASSES (CÁC LỚP CON CHUYÊN BIỆT)
# ==============================================================================
class VideoLesson(BaseLesson):
    """Kế thừa từ BaseLesson để quản lý bài học dạng video bài giảng"""
    def __init__(self, lesson_code: str, title: str, video_quality: str = "1080p"):
        super().__init__(lesson_code, title)
        self.video_quality = video_quality
        self.view_count = 0  # Số lượt học viên đã xem

    def calculate_completion_score(self) -> float:
        # Điểm hoàn thành = base_completion_points + (duration_minutes * 0.5)
        return self.base_completion_points + (self.duration_minutes * 0.5)

    def update_content(self, new_data):
        """Cập nhật độ phân giải video hoặc thông tin kỹ thuật"""
        if isinstance(new_data, str):
            self.video_quality = new_data
        elif isinstance(new_data, dict) and "video_quality" in new_data:
            self.video_quality = new_data["video_quality"]

    def play_video(self):
        """Giả lập hành vi xem bài học để tích lũy view"""
        self.view_count += 1


class CodingChallenge(BaseLesson):
    """Kế thừa từ BaseLesson để quản lý các bài tập thực hành code"""
    def __init__(self, lesson_code: str, title: str, number_of_testcases: int = 5, difficulty_multiplier: float = 1.5):
        super().__init__(lesson_code, title)
        if number_of_testcases <= 0:
            raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0.")
        self.number_of_testcases = number_of_testcases
        self.difficulty_multiplier = difficulty_multiplier

    def calculate_completion_score(self) -> float:
        # Điểm hoàn thành = base_completion_points * number_of_testcases * difficulty_multiplier
        return self.base_completion_points * self.number_of_testcases * self.difficulty_multiplier

    def update_content(self, new_data):
        """Thay đổi hoặc bổ sung thêm số lượng testcase cho bài tập"""
        if isinstance(new_data, (int, float)):
            if new_data <= 0:
                raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0.")
            self.number_of_testcases = int(new_data)


# ==============================================================================
# MULTIPLE INHERITANCE (ĐA KẾ THỪA CHUẨN MRO)
# ==============================================================================
class HybridAssessment(VideoLesson, CodingChallenge):
    """
    Dòng bài học lai cao cấp (Bài kiểm tra tổng hợp cuối module).
    Kế thừa từ cả VideoLesson và CodingChallenge đảm bảo cấu trúc hình thoi MRO.
    """
    def __init__(self, lesson_code: str, title: str, video_quality: str = "1080p", number_of_testcases: int = 5, difficulty_multiplier: float = 1.5):
        # Kích hoạt chuỗi hàm tạo theo thứ tự MRO để khởi tạo an toàn
        super().__init__(lesson_code, title, video_quality)
        CodingChallenge.__init__(self, lesson_code, title, number_of_testcases, difficulty_multiplier)

    def calculate_completion_score(self) -> float:
        """Tích hợp đồng thời cả cơ chế điểm thưởng theo thời gian của Video và hệ số độ khó từ Challenge"""
        video_score = VideoLesson.calculate_completion_score(self)
        challenge_bonus = self.number_of_testcases * self.difficulty_multiplier * 10
        return video_score + challenge_bonus

    def update_content(self, new_data):
        """Đa hình định tuyến cập nhật số lượng testcase cho dòng bài kiểm tra Hybrid"""
        CodingChallenge.update_content(self, new_data)


# ==============================================================================
# DUCK TYPING CLOUD STORAGE SERVICES
# ==============================================================================
class AWSS3StorageService:
    def upload_lesson(self, lesson: BaseLesson):
        print(f"[Hệ thống AWS S3]: Đang khởi tạo luồng băng thông kết nối tới LMS...")
        print(f"Xác thực dịch vụ bằng Duck Typing thành công!")
        print(f"Hệ thống lưu trữ đám mây [AWS S3] đã upload toàn bộ tài nguyên của bài học {lesson.lesson_code} lên cụm máy chủ an toàn.")

class GoogleCloudStorageService:
    def upload_lesson(self, lesson: BaseLesson):
        print(f"[Hệ thống Google Cloud Storage]: Đang kiểm tra định danh API Gateway...")
        print(f"Xác thực dịch vụ bằng Duck Typing thành công!")
        print(f"Hệ thống lưu trữ đám mây [GCS] đã đồng bộ hóa dữ liệu bài học {lesson.lesson_code} lên đám mây phân tán thành công.")

def sync_to_cloud(cloud_service, lesson: BaseLesson):
    """
    Hàm toàn cục độc lập áp dụng Duck Typing để đẩy dữ liệu lên mây.
    Bẫy dữ liệu: Kiểm tra sự tồn tại của phương thức upload_lesson (Edge Case 4).
    """
    if not hasattr(cloud_service, "upload_lesson") or not callable(getattr(cloud_service, "upload_lesson")):
        raise AttributeError("Dịch vụ lưu trữ đám mây không hợp lệ hoặc chưa ký kết chứng chỉ API liên thông.")
    cloud_service.upload_lesson(lesson)


# ==============================================================================
# HỆ THỐNG MENU COMMAND-LINE INTERFACE (CLI)
# ==============================================================================
def main():
    lessons = []
    current_lesson = None

    # Tạo sẵn một bài học đối chứng để dễ thực hiện chức năng test nạp chồng toán tử (Menu 5)
    try:
        sample_lesson = VideoLesson("LMS0099999", "Khoi Tao Framework")
        sample_lesson._set_duration_minutes(60.0)
        lessons.append(sample_lesson)
    except Exception:
        pass

    while True:
        print("\n===== RIKKEI ACADEMY LMS SIMULATOR PRO =====")
        print("1. Khởi tạo bài học mới (Chọn loại bài học nội dung)")
        print("2. Xem thông tin bài học & Kiểm tra thứ tự kế thừa (MRO)")
        print("3. Cập nhật thời lượng & Nội dung bài học (Tính đa hình)")
        print("4. Xem chi tiết điểm thưởng hoàn thành bài học")
        print("5. Kiểm tra gộp thời lượng & So sánh độ dài bài học (Overloading)")
        print("6. Đồng bộ bài giảng lên Nền tảng Đám mây (Duck Typing)")
        print("7. Thoát chương trình")
        print("==============================================")
        
        choice = input("Chọn chức năng (1-7): ").strip()
        
        if choice == '1':
            print("\n--- CHỌN LOẠI BÀI HỌC KHỞI TẠO ---")
            print("1. Video Lesson (Bài học Video Lý Thuyết)")
            print("2. Coding Challenge (Bài tập Thực Hành Code)")
            print("3. Hybrid Assessment (Bài Kiểm Tra Tổng Hợp)")
            
            type_choice = input("Chọn loại nhân sự (1-3): ").strip()
            lesson_code = input("Nhập mã bài học 10 ký tự: ").strip()
            title = input("Nhập tiêu đề bài học: ").strip()
            
            try:
                if type_choice == '1':
                    new_lesson = VideoLesson(lesson_code, title)
                    print("Khởi tạo bài học Video thành công!")
                elif type_choice == '2':
                    new_lesson = CodingChallenge(lesson_code, title)
                    print("Khởi tạo bài tập Thực Hành Code thành công!")
                elif type_choice == '3':
                    new_lesson = HybridAssessment(lesson_code, title)
                    print("Khởi tạo bài học Hybrid thành công!")
                else:
                    print("Lựa chọn loại bài học không hợp lệ.")
                    continue
                
                # Giả lập thiết lập thời lượng ban đầu (ví dụ: 45 phút) phục vụ tính toán
                new_lesson._set_duration_minutes(45.0)
                lessons.append(new_lesson)
                current_lesson = new_lesson
                print(f"Tiêu đề bài học: {current_lesson.title}")
                
            except ValueError as e:
                print(f"Mã bài học không hợp lệ! {e}")

        elif choice == '2':
            if not current_lesson:
                print("Chưa có bài học nào được khởi tạo hoặc chọn làm việc trong phiên hiện tại.")
                continue
                
            print("\n--- THÔNG TIN BÀI HỌC HIỆN TẠI ---")
            print(f"Loại bài học: {type(current_lesson).__name__}")
            print(f"Nền tảng: {current_lesson.platform_name}")
            print(f"Mã bài học: {current_lesson.lesson_code}")
            print(f"Tiêu đề bài học: {current_lesson.title}")
            print(f"Thời lượng bài học: {current_lesson.duration_minutes:.0f} phút")
            
            if isinstance(current_lesson, VideoLesson):
                print(f"Chất lượng video: {current_lesson.video_quality}")
                print(f"Số lượt xem video: {current_lesson.view_count} lượt")
            if isinstance(current_lesson, CodingChallenge):
                print(f"Số lượng testcase lập trình: {current_lesson.number_of_testcases} bài")
                print(f"Hệ số nhân độ khó: {current_lesson.difficulty_multiplier}")
                
            print(f"Danh sách kế thừa MRO: {[cls.__name__ for cls in type(current_lesson).__mro__]}")

        elif choice == '3':
            if not current_lesson:
                print("Hệ thống chưa ghi nhận bài học active để cập nhật.")
                continue
                
            print("\n--- CẬP NHẬT NỘI DUNG & THỜI LƯỢNG ---")
            print("1. Giả lập học viên tăng lượt xem video (Chỉ dành cho Video/Hybrid)")
            print("2. Cập nhật thông số bài học (Thời lượng, testcase...)")
            task_choice = input("Chọn tác vụ (1-2): ").strip()
            
            try:
                if task_choice == '1':
                    if isinstance(current_lesson, VideoLesson):
                        current_lesson.play_video()
                        print("Ghi nhận thành công! Học viên đã xem video bài học.")
                        print(f"Tổng số lượt xem hiện tại: {current_lesson.view_count} lượt.")
                    else:
                        print("Lỗi: Loại nội dung hiện tại không hỗ trợ hình thức xem video phát trực tuyến.")
                elif task_choice == '2':
                    print("Bạn muốn cập nhật thông số nào?")
                    print("  - Nhập số nguyên để thay đổi thông số lõi (Testcases).")
                    print("  - Nhập số thực để thay đổi thời lượng học (Phút).")
                    val_input = float(input("Nhập thông số mới cần cấu hình: ").strip())
                    
                    # Bẫy dữ liệu 2: Ngăn chặn số liệu âm (Edge Case 2)
                    if val_input <= 0:
                        raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0.")
                        
                    if val_input.is_integer() and isinstance(current_lesson, CodingChallenge):
                        current_lesson.update_content(int(val_input))
                        print("Cập nhật thông số thành công!")
                        print(f"Số lượng testcase hiện tại trên hệ thống: {current_lesson.number_of_testcases} testcases.")
                    else:
                        current_lesson._set_duration_minutes(val_input)
                        print("Cập nhật thời lượng học tập thành công!")
                        print(f"Thời lượng bài học mới: {current_lesson.duration_minutes:.1f} phút.")
            except ValueError as e:
                print(f"Lỗi: {e}")

        elif choice == '4':
            if not current_lesson:
                print("Không có dữ liệu bài học để chấm điểm thưởng hoàn thành.")
                continue
                
            print("\n--- CHI TIẾT ĐIỂM THƯỞNG HOÀN THÀNH ---")
            print(f"Bài học: {current_lesson.title} (Loại: {type(current_lesson).__name__})")
            print(f"Điểm cơ sở hệ thống: {BaseLesson.base_completion_points} XP")
            print(f"Thời lượng tích lũy: {current_lesson.duration_minutes:.0f} phút")
            
            if isinstance(current_lesson, CodingChallenge):
                print(f"Số lượng testcase cấu hình: {current_lesson.number_of_testcases} bài")
                
            xp_reward = current_lesson.calculate_completion_score()
            print(f"Tổng điểm kinh nghiệm (XP) nhận được khi hoàn thành: {xp_reward:.0f} XP")

        elif choice == '5':
            if not current_lesson or len(lessons) < 2:
                print("Hệ thống cần ít nhất 2 bài học trong bộ nhớ lưu trữ để tiến hành so sánh đối ứng.")
                continue
                
            print("\n--- ĐỒNG BỘ & SO SÁNH THỜI LƯỢNG (OPERATOR OVERLOADING) ---")
            print(f"Bài học hiện tại (A): {current_lesson.title} (Thời lượng: {current_lesson.duration_minutes:.0f} phút)")
            
            # Lấy phần tử mẫu đối ứng đã tạo sẵn từ trước
            other_les = [l for l in lessons if l.lesson_code != current_lesson.lesson_code][0]
            print(f"Chọn bài học đối ứng (B) từ danh sách: {other_les.lesson_code} ({other_les.title} - Thời lượng: {other_les.duration_minutes:.0f} phút)")
            
            # Thực thi nạp chồng toán tử __lt__ và __add__
            is_shorter = current_lesson < other_les
            total_time = current_lesson + other_les
            
            cmp_res = "NGẮN HƠN" if is_shorter else "KHÔNG NGẮN HƠN"
            print(f"[Kết quả So sánh (__lt__)]: Thời lượng bài học A {cmp_res} thời lượng bài học B.")
            print(f"[Kết quả Tổng hợp (__add__)]: Tổng thời lượng học tập của cả 2 bài học là: {total_time:.0f} phút.")
            
            # Thử nghiệm Bẫy dữ liệu 3: Cộng với kiểu dữ liệu không hợp lệ (Edge Case 3)
            print("\n[Kiểm thử nội bộ]: Kiểm tra khả năng từ chối gộp kiểu dữ liệu lạ...")
            try:
                invalid_calc = current_lesson + 9999  # Cộng đối tượng bài học với số nguyên thuần túy
                if invalid_calc == NotImplemented:
                    print("-> Kết quả: Đạt tiêu chuẩn! Hệ thống trả về NotImplemented chống crash.")
            except TypeError:
                print("-> Kết quả: Đạt tiêu chuẩn! Ứng dụng chặn đứng lỗi kiểu dữ liệu lạ.")

        elif choice == '6':
            if not current_lesson:
                print("Vui lòng khởi tạo thông tin bài học hoàn chỉnh trước khi đồng bộ đám mây.")
                continue
                
            print("\n--- ĐỒNG BỘ BÀI GIẢNG LÊN NỀN TẢNG ĐÁM MÂY ---")
            print("1. Đồng bộ lên máy chủ AWS S3 Storage")
            print("2. Đồng bộ lên máy chủ Google Cloud Storage")
            print("3. Giả lập kết nối tới cổng đám mây lỗi (Thử nghiệm phá vỡ API)")
            
            cloud_choice = input("Chọn dịch vụ lưu trữ (1-3): ").strip()
            
            try:
                if cloud_choice == '1':
                    service = AWSS3StorageService()
                    sync_to_cloud(service, current_lesson)
                elif cloud_choice == '2':
                    service = GoogleCloudStorageService()
                    sync_to_cloud(service, current_lesson)
                elif cloud_choice == '3':
                    # Tạo lớp rỗng không có hàm upload_lesson để kích hoạt bẫy dữ liệu
                    class BrokenCloudService: pass
                    bad_service = BrokenCloudService()
                    sync_to_cloud(bad_service, current_lesson)
                else:
                    print("Lựa chọn dịch vụ đám mây không nằm trong danh mục liên kết.")
            except AttributeError as e:
                # Bẫy dữ liệu 4: Bắt lỗi sai lệch phương thức Duck Typing (Edge Case 4)
                print(f"\n[Bẫy dữ liệu 4 - CẢNH BÁO CRITICAL]: {e}")

        elif choice == '7':
            print("Cảm ơn bạn đã trải nghiệm hệ thống Quản lý Bài học Rikkei Academy LMS Pro!")
            break
        else:
            print("Lựa chọn chức năng nằm ngoài phạm vi, vui lòng nhập lại từ 1 đến 7.")

if __name__ == "__main__":
    # Minh chứng Bẫy dữ liệu 1: Chặn đứng hành vi khởi tạo lớp trừu tượng trực tiếp (Edge Case 1)
    print("[Kiểm thử Bảo mật Kiến trúc]: Đang test khởi tạo trực tiếp BaseLesson...")
    try:
        abstract_test = BaseLesson("LMS0000001", "Abstract Test")
    except TypeError:
        print("-> Kết quả: Đạt tiêu chuẩn bảo mật! Python đã ném TypeError chặn khởi tạo trực tiếp lớp trừu tượng.\n")
        
    main()