from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from django.conf import settings

class PDSPDFGenerator:
    """Generate beautiful PDF for Personal Data Sheet"""
    
    def __init__(self, form_instance):
        self.form = form_instance
        self.buffer = BytesIO()
        self.width, self.height = letter
        self.styles = getSampleStyleSheet()
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.white,
            backColor=colors.HexColor('#2c3e50'),
            spaceAfter=10,
            spaceBefore=10,
            leftIndent=10,
            fontName='Helvetica-Bold'
        )
        
        self.label_style = ParagraphStyle(
            'Label',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#555555'),
            fontName='Helvetica-Bold'
        )
        
        self.value_style = ParagraphStyle(
            'Value',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1a1a1a'),
            fontName='Helvetica'
        )
    
    def generate(self):
        """Generate the complete PDF"""
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
        )
        
        story = []
        
        # Header with Photo
        story.append(self._create_header())
        story.append(Spacer(1, 0.3 * inch))
        
        # Personal Information
        story.append(Paragraph("I. PERSONAL INFORMATION", self.section_style))
        story.append(self._create_personal_info_table())
        story.append(Spacer(1, 0.2 * inch))
        
        # Family Background
        story.append(Paragraph("II. FAMILY BACKGROUND", self.section_style))
        story.append(self._create_family_background_table())
        story.append(Spacer(1, 0.2 * inch))
        
        # Educational Background
        story.append(PageBreak())
        story.append(Paragraph("III. EDUCATIONAL BACKGROUND", self.section_style))
        story.append(self._create_educational_background_table())
        story.append(Spacer(1, 0.2 * inch))
        
        # Civil Service Eligibility
        if self.form.civil_service.exists():
            story.append(Paragraph("IV. CIVIL SERVICE ELIGIBILITY", self.section_style))
            story.append(self._create_civil_service_table())
            story.append(Spacer(1, 0.2 * inch))
        
        # Work Experience
        if self.form.work_experience.exists():
            story.append(PageBreak())
            story.append(Paragraph("V. WORK EXPERIENCE", self.section_style))
            story.append(self._create_work_experience_table())
            story.append(Spacer(1, 0.2 * inch))
        
        # Voluntary Work
        if self.form.voluntary_work.exists():
            story.append(Paragraph("VI. VOLUNTARY WORK", self.section_style))
            story.append(self._create_voluntary_work_table())
            story.append(Spacer(1, 0.2 * inch))
        
        # Learning & Development
        if self.form.learning_development.exists():
            story.append(PageBreak())
            story.append(Paragraph("VII. LEARNING AND DEVELOPMENT", self.section_style))
            story.append(self._create_learning_development_table())
            story.append(Spacer(1, 0.2 * inch))
        
        # Other Information
        story.append(PageBreak())
        story.append(Paragraph("VIII. OTHER INFORMATION", self.section_style))
        story.append(self._create_other_information_table())
        story.append(Spacer(1, 0.3 * inch))
        
        # Signature Section
        story.append(self._create_signature_section())
        
        # Build PDF
        doc.build(story, onFirstPage=self._add_page_number, onLaterPages=self._add_page_number)
        
        self.buffer.seek(0)
        return self.buffer
    
    def _create_header(self):
        """Create header with photo and title"""
        data = []
        
        # Photo section
        photo_cell = ""
        if self.form.id_photo and self.form.id_photo.name:
            try:
                photo_path = self.form.id_photo.path
                img = Image(photo_path, width=1.5*inch, height=1.5*inch)
                photo_cell = img
            except:
                photo_cell = Paragraph("No Photo", self.value_style)
        else:
            photo_cell = Paragraph("No Photo", self.value_style)
        
        # Title section
        title_cell = [
            Paragraph("<b>PERSONAL DATA SHEET</b>", self.title_style),
            Paragraph(f"<b>{self.form.name}</b>", ParagraphStyle(
                'FormName',
                parent=self.styles['Normal'],
                fontSize=12,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#2c3e50')
            ))
        ]
        
        table = Table(
            [[photo_cell, title_cell]],
            colWidths=[2*inch, 5.5*inch]
        )
        
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        return table
    
    def _create_personal_info_table(self):
        """Create personal information section"""
        p = self.form.personal_information
        
        data = [
            ['Full Name:', f"{p.firstname} {p.middlename or ''} {p.surname}".strip(), 'Date of Birth:', str(p.date_of_birth)],
            ['Place of Birth:', p.place_of_birth, 'Sex:', p.sex],
            ['Civil Status:', p.civil_status, 'Height:', f"{p.height} cm"],
            ['Weight:', f"{p.weight} kg", 'Blood Type:', p.blood_type],
            ['Citizenship:', p.citizenship, 'Email:', p.email_address or 'N/A'],
            ['Mobile No.:', p.mobile_no or 'N/A', 'Telephone:', p.telephone_no or 'N/A'],
        ]
        
        # Residential Address
        data.append([Paragraph('<b>Residential Address:</b>', self.label_style), 
                     Paragraph(p.residential_address, self.value_style), 
                     'ZIP Code:', p.residential_zip_code])
        
        # Permanent Address
        data.append([Paragraph('<b>Permanent Address:</b>', self.label_style), 
                     Paragraph(p.permanent_address or 'Same as above', self.value_style), 
                     'ZIP Code:', p.permanent_zip_code or ''])
        
        # Government IDs
        data.extend([
            ['GSIS No.:', p.gsis or 'N/A', 'SSS No.:', p.sss_no or 'N/A'],
            ['Pag-IBIG No.:', p.pag_ibig or 'N/A', 'PhilHealth No.:', p.philhealth or 'N/A'],
            ['TIN:', p.tin_no or 'N/A', 'Employee No.:', p.agent_employee_number or 'N/A'],
        ])
        
        table = Table(data, colWidths=[1.5*inch, 2.2*inch, 1.3*inch, 2.5*inch])
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
            ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#555555')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        return table
    
    def _create_family_background_table(self):
        """Create family background section"""
        f = self.form.family_background
        
        data = [
            ['Spouse Surname:', f.spouse_surname or 'N/A', 'First Name:', f.spouse_firstname or 'N/A'],
            ['Middle Name:', f.spouse_middlename or 'N/A', 'Occupation:', f.spouse_occupation or 'N/A'],
            ['Employer:', f.spouse_employer_business_name or 'N/A', 'Telephone:', f.spouse_telephone_no or 'N/A'],
        ]
        
        # Father's Information
        data.append([Paragraph('<b>Father\'s Name:</b>', self.label_style), 
                     f"{f.father_firstname or ''} {f.father_middlename or ''} {f.father_surname or ''}".strip() or 'N/A',
                     '', ''])
        
        # Mother's Information
        data.append([Paragraph('<b>Mother\'s Maiden Name:</b>', self.label_style), 
                     f"{f.mother_firstname or ''} {f.mother_middlename or ''} {f.mother_maiden_lastname or ''}".strip() or 'N/A',
                     '', ''])
        
        # Children
        if f.children:
            data.append([Paragraph('<b>Children:</b>', self.label_style), 
                        Paragraph(f.children, self.value_style), '', ''])
        
        table = Table(data, colWidths=[1.5*inch, 2.5*inch, 1.2*inch, 2.3*inch])
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        return table
    
    def _create_educational_background_table(self):
        """Create educational background section"""
        e = self.form.educational_background
        
        data = [
            ['Level', 'School Name', 'Degree/Course', 'Period', 'Year Graduated', 'Honors']
        ]
        
        # Elementary
        data.append([
            'Elementary',
            e.elementary_name or 'N/A',
            e.elementary_degree_course or 'N/A',
            f"{e.elementary_period_from or ''} - {e.elementary_period_to or ''}",
            e.elementary_year_graduated or 'N/A',
            e.elementary_honors or 'N/A'
        ])
        
        # Secondary
        data.append([
            'Secondary',
            e.secondary_name or 'N/A',
            e.secondary_degree_course or 'N/A',
            f"{e.secondary_period_from or ''} - {e.secondary_period_to or ''}",
            e.secondary_year_graduated or 'N/A',
            e.secondary_honors or 'N/A'
        ])
        
        # Vocational
        if e.vocational_name:
            data.append([
                'Vocational',
                e.vocational_name,
                e.vocational_degree_course or 'N/A',
                f"{e.vocational_period_from or ''} - {e.vocational_period_to or ''}",
                e.vocational_year_graduated or 'N/A',
                e.vocational_honors or 'N/A'
            ])
        
        # College
        if e.college_name:
            data.append([
                'College',
                e.college_name,
                e.college_degree_course or 'N/A',
                f"{e.college_period_from or ''} - {e.college_period_to or ''}",
                e.college_year_graduated or 'N/A',
                e.college_honors or 'N/A'
            ])
        
        # Graduate
        if e.graduate_name:
            data.append([
                'Graduate',
                e.graduate_name,
                e.graduate_degree_course or 'N/A',
                f"{e.graduate_period_from or ''} - {e.graduate_period_to or ''}",
                e.graduate_year_graduated or 'N/A',
                e.graduate_honors or 'N/A'
            ])
        
        table = Table(data, colWidths=[1*inch, 1.8*inch, 1.5*inch, 1.2*inch, 0.9*inch, 1.1*inch])
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        return table
    
    def _create_civil_service_table(self):
        """Create civil service eligibility section"""
        data = [['Eligibility', 'Rating', 'Exam Date', 'Place', 'License No.', 'Validity']]
        
        for item in self.form.civil_service.all():
            data.append([
                item.career_service or 'N/A',
                str(item.rating) if item.rating else 'N/A',
                str(item.exam_date) if item.exam_date else 'N/A',
                item.exam_place or 'N/A',
                item.license_number or 'N/A',
                str(item.license_validity) if item.license_validity else 'N/A'
            ])
        
        table = Table(data, colWidths=[1.8*inch, 0.7*inch, 1*inch, 1.5*inch, 1*inch, 1*inch])
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        return table
    
    def _create_work_experience_table(self):
        """Create work experience section"""
        data = [['Period', 'Position', 'Company/Agency', 'Salary', 'Grade', 'Status', 'Govt']]
        
        for w in self.form.work_experience.all():
            period = f"{w.from_date or ''}\nto\n{w.to_date or 'Present'}"
            data.append([
                period,
                w.position_title or 'N/A',
                w.department or 'N/A',
                str(w.monthly_salary) if w.monthly_salary else 'N/A',
                w.salary_grade or 'N/A',
                w.status_of_appointment or 'N/A',
                w.govt_service or 'N'
            ])
        
        table = Table(data, colWidths=[1*inch, 1.5*inch, 1.8*inch, 0.8*inch, 0.6*inch, 1*inch, 0.5*inch])
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        return table
    
    def _create_voluntary_work_table(self):
        """Create voluntary work section"""
        data = [['Organization', 'Period', 'Hours', 'Nature of Work']]
        
        for v in self.form.voluntary_work.all():
            period = f"{v.from_date or ''} to {v.to_date or 'Present'}"
            data.append([
                v.organization_name or 'N/A',
                period,
                str(v.number_of_hours) if v.number_of_hours else 'N/A',
                v.nature_of_work or 'N/A'
            ])
        
        table = Table(data, colWidths=[2.5*inch, 1.5*inch, 0.8*inch, 2.7*inch])
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        return table
    
    def _create_learning_development_table(self):
        """Create learning & development section"""
        data = [['Title', 'Period', 'Hours', 'Type', 'Conducted By']]
        
        for l in self.form.learning_development.all():
            period = f"{l.from_date or ''} to {l.to_date or ''}"
            data.append([
                l.title or 'N/A',
                period,
                str(l.number_of_hours) if l.number_of_hours else 'N/A',
                l.type_of_ld or 'N/A',
                l.conducted_by or 'N/A'
            ])
        
        table = Table(data, colWidths=[2*inch, 1.2*inch, 0.7*inch, 1.1*inch, 2.5*inch])
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        return table
    
    def _create_other_information_table(self):
        """Create other information section"""
        o = self.form.other_information
        
        data = [
            ['Third Degree Relative:', o.with_third_degree, 'Fourth Degree:', o.with_fourth_degree],
            ['Administrative Offense:', o.offense, 'Criminally Charged:', o.criminal],
            ['Convicted:', o.convicted, 'Separated from Service:', o.sep_service],
            ['Election Candidate:', o.candidate, 'Resigned for Campaign:', o.resign_candid],
            ['Immigrant:', o.immigrant_status, 'Indigenous Member:', o.indigenous_group_member],
            ['PWD:', o.disability_status, 'Solo Parent:', o.solo_parent_status],
        ]
        
        if o.references:
            data.append([Paragraph('<b>References:</b>', self.label_style), 
                        Paragraph(o.references, self.value_style), '', ''])
        
        if o.government_id:
            data.append(['Government ID:', o.government_id, 'ID Number:', o.government_id_number or 'N/A'])
        
        table = Table(data, colWidths=[1.8*inch, 1.7*inch, 1.8*inch, 2.2*inch])
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        return table
    
    def _create_signature_section(self):
        """Create signature section with digital signature if available"""
        elements = []
        
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("I certify that the above information is true and correct to the best of my knowledge.", 
                                 self.value_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Signature
        sig_data = []
        
        if self.form.is_signed and self.form.digital_signature:
            try:
                # Decode base64 signature
                import base64
                from PIL import Image as PILImage
                
                signature_data = self.form.digital_signature.split(',')[1]
                signature_bytes = base64.b64decode(signature_data)
                
                # Create temporary image
                sig_buffer = BytesIO(signature_bytes)
                sig_img = Image(sig_buffer, width=2*inch, height=1*inch)
                
                sig_data.append(['', sig_img])
                sig_data.append(['', '________________________'])
                sig_data.append(['', 'Digital Signature'])
                if self.form.signature_date:
                    sig_data.append(['', f'Signed: {self.form.signature_date.strftime("%B %d, %Y")}'])
            except Exception as e:
                print(f"Error loading signature: {e}")
                sig_data.append(['', '________________________'])
                sig_data.append(['', 'Signature'])
        else:
            sig_data.append(['', '________________________'])
            sig_data.append(['', 'Signature over Printed Name'])
            sig_data.append(['', ''])
            sig_data.append(['', 'Date: ________________'])
        
        sig_table = Table(sig_data, colWidths=[4*inch, 3*inch])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))
        
        elements.append(sig_table)
        
        return KeepTogether(elements)
    
    def _add_page_number(self, canvas, doc):
        """Add page number to each page"""
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.grey)
        canvas.drawRightString(doc.width + doc.rightMargin - 20, 20, text)
        canvas.restoreState()