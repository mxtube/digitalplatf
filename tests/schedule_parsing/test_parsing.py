import pytest


class TestScheduleParsing:

    @pytest.mark.django_db
    def test_init_schedule_parsing(self, tmp_correct_sch_file_by_day, department):
        assert tmp_correct_sch_file_by_day.file.sheetnames == ['Лист1']
        assert tmp_correct_sch_file_by_day.error_box == []
        assert tmp_correct_sch_file_by_day.start_row == tmp_correct_sch_file_by_day.start_row
        assert tmp_correct_sch_file_by_day.iter_col == 2
        assert tmp_correct_sch_file_by_day.department.name == department.name

    @pytest.mark.django_db
    def test_parsing_correct_schedule_file(self, tmp_correct_sch_file_by_day, department):
        parser = tmp_correct_sch_file_by_day._excel_reader()
        assert parser
        assert len(tmp_correct_sch_file_by_day.error_box) == 0
