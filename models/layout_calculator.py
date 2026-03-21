from enums.spacing_size import SpacingSize
from models.resume_renderer import ResumeRenderer
from models.resume_pdf_factory import ResumePdfFactory

_SPACING_ADJUST_IN = 0.01


class LayoutCalculator:
    @staticmethod
    def _calculate_smart_spacing_in(
        pdf_factory: ResumePdfFactory, resume_data: list[str]
    ) -> float:
        min_spacing_in = SpacingSize.COMPACT.value
        pdf = pdf_factory.create(min_spacing_in)
        pdf = ResumeRenderer.render(pdf, resume_data)
        min_page_count = pdf.pages_count

        max_spacing_in = SpacingSize.SPACIOUS.value
        pdf = pdf_factory.create(max_spacing_in)
        pdf = ResumeRenderer.render(pdf, resume_data)
        max_page_count = pdf.pages_count

        # Can't reduce page count so fill as much space as possible
        if min_page_count == max_page_count:
            return max_spacing_in

        # Calculate exact spacing to fill the page
        smart_spacing_in = SpacingSize.COMPACT.value
        min_spacing_in = SpacingSize.COMPACT.value
        max_spacing_in = SpacingSize.SPACIOUS.value
        while min_spacing_in < max_spacing_in:
            smart_spacing_in = (min_spacing_in + max_spacing_in) / 2

            pdf = pdf_factory.create(smart_spacing_in)
            pdf = ResumeRenderer.render(pdf, resume_data)

            is_overflowing_page = pdf.pages_count > 1 and pdf.get_y() > 0
            if is_overflowing_page:
                max_spacing_in = smart_spacing_in - _SPACING_ADJUST_IN
            else:
                min_spacing_in = smart_spacing_in + _SPACING_ADJUST_IN
        return smart_spacing_in
