# -*- coding: utf-8 -*-

def clean_title(title):
  """ Limpa o título de um filme ou série removendo caracteres especiais. """
  # (substituir caracteres especiais por espaços ou caracteres permitidos)
  cleaned_title = title.replace("[^a-zA-Z0-9 !?]", " ")
  return cleaned_title.strip()

def convert_to_int(value):
  """ Tenta converter um valor para inteiro, retornando 0 caso não seja possível. """
  try:
    return int(value)
  except ValueError:
    return 0
  
# Código fim
