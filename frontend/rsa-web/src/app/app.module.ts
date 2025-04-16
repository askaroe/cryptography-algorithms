import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { RsaComponent } from './rsa/rsa.component';
import { FormsModule } from '@angular/forms'; // ✅ Import FormsModule
import { HttpClientModule } from '@angular/common/http';
import { SignatureVerificationComponent } from './signature-verification/signature-verification.component';
import { CryptoComponent } from './crypto/crypto.component';

@NgModule({
  declarations: [
    AppComponent,
    RsaComponent,
    SignatureVerificationComponent,
    CryptoComponent
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
