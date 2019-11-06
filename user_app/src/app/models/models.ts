/* View models */

export interface Object {
  [key: string]: number | string | boolean | Object;
}

export interface Text {
  [key: string]: string;
}

export interface Profile {
  user_id: number;
  first_name: string;
  last_name: string;
  user: string;
  language: string;
  language_full: string;
  phone: string;
  photo?: string;
  airline_image?: string;
  travel_image?: string;
  passport_image?: string;
  medical_image?: string;
  document_id?: string;
}

export interface Plan {
  created: string;
  package?: Package;
  calls?: number;
  company?: string;
  company_id?: number;
  emails?: number;
  id?: number;
  price?: string;
  title?: string;
  traffic?: number;
}

export interface Package {
  calls: number;
  company: string;
  company_id: number;
  emails: number;
  id: number;
  price: string;
  title: string;
  traffic: number;
}

export interface History {
  type: string;
  status: string;
  created: any;
  package: {
    title: string;
  };
}

export interface Language {
  id: number;
  file_url: string;
  title: string;
  title_full: string;
}

export interface Alert {
  title: string;
  subTitle: string;
  link: string;
  pubDate: string;
}

export interface Address {
  city: string;
  street: string;
  number: string;
  note: string;
  zip: string;
}

export interface Company {
  id: number;
  logo: string;
  title: string;
}

export interface SimPlan {
  card: number;
  pack: number;
  price: number;
  cvv: number;
}

export interface Image {
  file: Blob;
  src: string;
}

export interface MedicalHistory {
  consume_alcohol: 'NOT-SET' | 'DAILY' | 'WEEKLY' | 'MONTHLY' | 'OCCASIONALLY' | 'NEVER';
  current_symptoms: Array<{ title: string }>;
  gender: 'NOT-SET' | 'MALE' | 'FEMALE';
  illegal_drugs: boolean;
  medication_allergies: 'NOT-SURE' | 'YES' | 'NO';
  relative_diseases: Array<{ title: string }>;
  taking_medication: boolean;
  use_tobacco: boolean;
}

/* Request models */

export interface ProfileEditRequest {
  user?: string;
  first_name?: string;
  last_name?: string;
  language?: string;
  document_id?: string;
  phone?: string;
}

export interface OrderSimCardRequest {
  type: string;
  name: string;
  email: string;
  address: string;
  city: string;
  phone_number: string;
  company: number;
}

export interface CheckupRequest {
  visit_date: string;
  colonoscopy: boolean;
  oncomarker: boolean;
}

export interface RegisterDeviceFcmRequest {
  player_id: string;
  device_id: string;
}

/* Response models */

export interface BaseResponse {
  content: any;
  metadata: any;
}
