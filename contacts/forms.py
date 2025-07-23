from django import forms
from django.core.exceptions import  ValidationError
from .models import Contact
import mimetypes
import os

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Contact Name'
        })
    )

    email = forms.EmailField(
        widget = forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Email Address'
        })
    )

    document = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'file-input file-input-bordered w-full',
            'accept': '.pdf,.doc,.docx,.txt,.rtf,.odt,.xls,.xlsx,.csv,.ppt,.pptx'
        }),
        required=False,
        help_text="Only document files are allowed (PDF, DOC, DOCX, TXT, RTF, ODT, XLS, XLSX, CSV, PPT, PPTX)"
    )

    def clean_name(self):
            name = self.cleaned_data['name']
            # checking whether email exists
            if Contact.objects.filter(user=self.initial.get('user'), name=name).exists():
                raise ValidationError("You already have a contact with this name.")
            return name

    def clean_email(self):
        email = self.cleaned_data['email']
        # checking whether email exists
        if Contact.objects.filter(user=self.initial.get('user'), email=email).exists():
            raise ValidationError("You already have a contact with this email address.")
        return email
    
    def clean_document(self):
        document = self.cleaned_data.get('document')
        
        if document:
            # Define allowed document file extensions
            allowed_extensions = [
                '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt',  # Text documents
                '.xls', '.xlsx', '.csv',  # Spreadsheets
                '.ppt', '.pptx',  # Presentations
            ]
            
            # Define allowed MIME types
            allowed_mime_types = [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'text/plain',
                'application/rtf',
                'application/vnd.oasis.opendocument.text',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'text/csv',
                'application/vnd.ms-powerpoint',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            ]
            
            # Check file extension
            file_name = document.name.lower()
            file_ext = os.path.splitext(file_name)[1]
            
            if file_ext not in allowed_extensions:
                raise ValidationError(
                    f"File type '{file_ext}' is not allowed. "
                    f"Please upload a document file: {', '.join(allowed_extensions)}"
                )
            
            # Check MIME type
            mime_type, _ = mimetypes.guess_type(file_name)
            if mime_type and mime_type not in allowed_mime_types:
                raise ValidationError(
                    "Invalid file type detected. Please upload a valid document file."
                )
            
            # Check file size (optional - limit to 10MB)
            max_size = 10 * 1024 * 1024  # 10MB in bytes
            if document.size > max_size:
                raise ValidationError(
                    f"File size is too large. Maximum allowed size is 10MB. "
                    f"Your file is {document.size / (1024*1024):.1f}MB."
                )
            
            # Additional security check - read first few bytes to verify it's not an image
            document.seek(0)  # Reset file pointer
            first_bytes = document.read(10)
            document.seek(0)  # Reset again for later use
            
            # Check for common image file signatures
            image_signatures = [
                b'\xFF\xD8\xFF',  # JPEG
                b'\x89PNG\r\n\x1a\n',  # PNG
                b'GIF87a',  # GIF87a
                b'GIF89a',  # GIF89a
                b'RIFF',  # WebP (starts with RIFF)
                b'BM',  # BMP
            ]
            
            for signature in image_signatures:
                if first_bytes.startswith(signature):
                    raise ValidationError(
                        "Image files are not allowed. Please upload a document file."
                    )
        
        return document

    class Meta:
        model = Contact
        fields = (
            'name', 'email', 'document'
        )
