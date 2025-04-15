import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { RsaComponent } from './rsa/rsa.component';
import { FormsModule } from '@angular/forms'; // ✅ Import FormsModule
import { HttpClientModule } from '@angular/common/http';
import { KeyGenerationComponent } from './key-generation/key-generation.component';
import { DigitalSignatureComponent } from './digital-signature/digital-signature.component';
import { SignatureVerificationComponent } from './signature-verification/signature-verification.component';

@NgModule({
  declarations: [
    AppComponent,
    RsaComponent,
    KeyGenerationComponent,
    DigitalSignatureComponent,
    SignatureVerificationComponent
  ],
  imports: [
    BrowserModule,
    FormsModule, 
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
